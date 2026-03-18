#!/bin/bash
# /usr/local/bin/mutmut-wrapper — Fish tank mutmut interface
#
# Provides a clean, agent-friendly interface to mutmut 3.x.
# Suppresses spinner noise, enforces correct v3 commands, and
# writes detailed output to files to keep context window small.
#
# All detailed output goes to /project/mutmut_output/. The agent
# should use the Read tool with offset/limit to inspect results
# rather than dumping everything into a single Bash call.
#
# Usage:
#   mutmut-wrapper run [module_pattern]
#   mutmut-wrapper results
#   mutmut-wrapper show <path/to/file.py>
#   mutmut-wrapper show-all
#   mutmut-wrapper html
#
# Installed to /usr/local/bin/ by the Dockerfile.

set -euo pipefail

OUTPUT_DIR="/project/mutmut_output"

ensure_output_dir() {
    mkdir -p "$OUTPUT_DIR"
}

usage() {
    cat <<'EOF'
mutmut-wrapper — agent-friendly mutmut 3.x interface

All detailed output is written to /project/mutmut_output/.
Use the Read tool to inspect results file-by-file.

Commands:
  run [pattern]        Run mutation testing (optional glob pattern for modules)
  results              Show summary of last run
  show <file>          Show survived mutant diffs for a specific file
  show-all             Show all survived mutant diffs (writes to file)
  html                 Generate HTML report in /project/mutmut-report/

Examples:
  mutmut-wrapper run
  mutmut-wrapper run "mymodule.myfunction*"
  mutmut-wrapper results
  mutmut-wrapper show src/myapp/config.py
  mutmut-wrapper show-all
EOF
    exit 0
}

cmd_run() {
    ensure_output_dir
    local pattern="${1:-}"
    local run_log="$OUTPUT_DIR/run.log"

    # Targeted runs require .coverage data for test-to-code mapping.
    # Without it, mutmut can't associate mutants with tests and stops early.
    if [ -n "$pattern" ] && [ ! -f /project/.coverage ]; then
        echo "WARNING: No .coverage file found. Targeted mutmut runs need coverage"
        echo "data to map mutants to tests. Run 'coverage-wrapper run' first."
        echo ""
        echo "Running anyway (may fail with 'could not find any test case')..."
        echo ""
    fi

    if [ -n "$pattern" ]; then
        echo "Running mutmut: $pattern"
        mutmut run "$pattern" 2>/dev/null | tail -20 > "$run_log"
        local rc=${PIPESTATUS[0]}
    else
        echo "Running mutmut: all configured paths"
        mutmut run 2>/dev/null | tail -20 > "$run_log"
        local rc=${PIPESTATUS[0]}
    fi

    # Check for the "no test case" early stop
    if grep -q "could not find any test case" "$run_log" 2>/dev/null; then
        echo "mutmut could not map mutants to test cases."
        echo ""
        if [ -n "$pattern" ]; then
            echo "This commonly happens with targeted runs. Options:"
            echo "  1. Run 'coverage-wrapper run' first to generate .coverage data"
            echo "  2. Run 'mutmut-wrapper run' without a pattern (full run)"
            echo "  3. Check that the pattern matches paths in pyproject.toml paths_to_mutate"
        fi
        cat "$run_log"
        return 1
    fi

    # Exit code 1 = mutations survived (normal). Only fail on 2+ (real errors).
    if [ $rc -eq 0 ]; then
        echo "All mutants killed."
        cat "$run_log"
    elif [ $rc -eq 1 ]; then
        echo "Run complete (some mutants survived)."
        cat "$run_log"
        echo ""
        cmd_results
    else
        echo "mutmut failed (exit code $rc). Details:"
        cat "$run_log"
        exit $rc
    fi
}

cmd_results() {
    ensure_output_dir
    local results_file="$OUTPUT_DIR/results.txt"

    mutmut results 2>/dev/null > "$results_file" || true

    if [ ! -s "$results_file" ]; then
        echo "No results available. Run 'mutmut-wrapper run' first."
        return
    fi

    # Print the results summary (this is already compact)
    cat "$results_file"
}

cmd_show() {
    ensure_output_dir
    local file="${1:-}"
    if [ -z "$file" ]; then
        echo "Error: 'show' requires a file path"
        echo "Usage: mutmut-wrapper show path/to/file.py"
        echo "       mutmut-wrapper show-all    (for all files)"
        exit 1
    fi

    local safe_name
    safe_name=$(echo "$file" | tr '/' '_')
    local out_file="$OUTPUT_DIR/survived_${safe_name}.txt"

    mutmut show all "$file" 2>/dev/null > "$out_file" || true

    if [ ! -s "$out_file" ]; then
        echo "No survived mutants for $file"
        return
    fi

    local line_count
    line_count=$(wc -l < "$out_file")

    if [ "$line_count" -le 60 ]; then
        # Small enough to print directly
        cat "$out_file"
    else
        # Too large — print summary, point to file
        echo "Survived mutants for $file: $line_count lines of diffs"
        echo "Written to: $out_file"
        echo "Use Read tool with offset/limit to inspect."
        echo ""
        echo "Preview (first 30 lines):"
        head -30 "$out_file"
    fi
}

cmd_show_all() {
    ensure_output_dir
    local out_file="$OUTPUT_DIR/survived_all.txt"

    mutmut show all 2>/dev/null > "$out_file" || true

    if [ ! -s "$out_file" ]; then
        echo "No survived mutants."
        return
    fi

    local line_count
    line_count=$(wc -l < "$out_file")

    if [ "$line_count" -le 60 ]; then
        cat "$out_file"
    else
        echo "All survived mutants: $line_count lines of diffs"
        echo "Written to: $out_file"
        echo "Use Read tool with offset/limit to inspect."
        echo ""
        echo "Preview (first 30 lines):"
        head -30 "$out_file"
    fi
}

cmd_html() {
    echo "Generating HTML report..."
    mutmut html 2>/dev/null
    echo "Report generated. Check mutmut-report/ directory."
}

# --- Main ---

if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    usage
fi

case "$1" in
    run)
        shift
        cmd_run "$@"
        ;;
    results)
        cmd_results
        ;;
    show)
        shift
        cmd_show "$@"
        ;;
    show-all)
        cmd_show_all
        ;;
    html)
        cmd_html
        ;;
    *)
        echo "Error: unknown command '$1'"
        echo ""
        usage
        ;;
esac
