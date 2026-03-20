#!/bin/bash
# /usr/local/bin/coverage-wrapper — Fish tank coverage interface
#
# Provides a clean, agent-friendly interface to pytest-cov.
# Writes detailed output to files to keep context window small.
# The agent should use the Read tool to inspect results.
#
# Usage:
#   coverage-wrapper run [pytest-args]
#   coverage-wrapper report
#   coverage-wrapper report <path/to/file.py>
#   coverage-wrapper gaps
#   coverage-wrapper gaps <path/to/file.py>
#   coverage-wrapper html
#
# Installed to /usr/local/bin/ by the Dockerfile.

set -euo pipefail

OUTPUT_DIR="/project/mutmut_output"

ensure_output_dir() {
    mkdir -p "$OUTPUT_DIR"
}

usage() {
    cat <<'EOF'
coverage-wrapper — agent-friendly pytest-cov interface

All detailed output is written to /project/mutmut_output/.
Use the Read tool to inspect results.

Commands:
  run [pytest-args]       Run tests with branch coverage (extra pytest args optional)
  report                  Show coverage summary (module-level percentages)
  report <file>           Show line-by-line coverage for one file
  gaps                    Show only files with missing coverage, sorted worst-first
  gaps <file>             Show uncovered line numbers for one file
  html                    Generate HTML report in htmlcov/

Examples:
  coverage-wrapper run
  coverage-wrapper run tests/test_config.py -x
  coverage-wrapper report
  coverage-wrapper gaps
  coverage-wrapper gaps src/myapp/config.py
  coverage-wrapper html
EOF
    exit 0
}

# Detect src directory for --cov argument
detect_src() {
    if [ -f /project/pyproject.toml ]; then
        if grep -q 'where.*=.*\["src"\]' /project/pyproject.toml 2>/dev/null; then
            echo "src"
            return
        fi
    fi
    if [ -d /project/src ]; then
        echo "src"
        return
    fi
    # Flat layout — try to find the main package
    echo "."
}

cmd_run() {
    ensure_output_dir
    local src_dir
    src_dir=$(detect_src)
    local run_log="$OUTPUT_DIR/coverage_run.log"

    echo "Running tests with branch coverage..."
    # Capture full output to file, show only summary
    pytest --cov="$src_dir" --cov-branch --cov-report=term-missing \
        --tb=short -q "$@" 2>&1 > "$run_log"
    local rc=$?

    if [ $rc -eq 0 ]; then
        echo "All tests passed."
    elif [ $rc -eq 1 ]; then
        echo "Some tests failed."
    else
        echo "pytest error (exit code $rc)."
    fi

    # Extract just the coverage table (starts with "Name" header, ends with "TOTAL")
    local cov_file="$OUTPUT_DIR/coverage_summary.txt"
    sed -n '/^Name.*Stmts.*Miss.*Cover/,/^TOTAL/p' "$run_log" > "$cov_file" 2>/dev/null || true

    if [ -s "$cov_file" ]; then
        echo ""
        cat "$cov_file"
        echo ""
        echo "Full output: $run_log"
        echo "Use 'coverage-wrapper gaps' to see uncovered lines."
    else
        echo ""
        echo "No coverage data captured. Full output: $run_log"
        echo "Use Read tool to inspect."
    fi

    return $rc
}

cmd_report() {
    ensure_output_dir
    local file="${1:-}"

    if [ -n "$file" ]; then
        # Single file report
        local report_file="$OUTPUT_DIR/coverage_$(echo "$file" | tr '/' '_').txt"
        coverage report --show-missing --include="$file" 2>/dev/null > "$report_file" || true
        if [ -s "$report_file" ]; then
            cat "$report_file"
        else
            echo "No coverage data for $file. Run 'coverage-wrapper run' first."
        fi
    else
        # Full report
        local report_file="$OUTPUT_DIR/coverage_report.txt"
        coverage report --show-missing 2>/dev/null > "$report_file" || true
        if [ -s "$report_file" ]; then
            local line_count
            line_count=$(wc -l < "$report_file")
            if [ "$line_count" -le 60 ]; then
                cat "$report_file"
            else
                echo "Coverage report: $line_count lines"
                echo "Written to: $report_file"
                echo ""
                # Show TOTAL line and worst files
                echo "Summary:"
                grep "^TOTAL" "$report_file" || true
                echo ""
                echo "Worst coverage (bottom 10):"
                grep -v "^-\|^Name\|^TOTAL\|^$" "$report_file" | sort -t'%' -k1 -n | head -10
            fi
        else
            echo "No coverage data. Run 'coverage-wrapper run' first."
        fi
    fi
}

cmd_gaps() {
    ensure_output_dir
    local file="${1:-}"

    if [ -n "$file" ]; then
        # Single file gaps
        echo "Uncovered lines in $file:"
        coverage report --show-missing --include="$file" 2>/dev/null | \
            grep -v "^-\|^Name\|^TOTAL\|^$" || echo "(no data for this file)"
    else
        # All gaps, sorted worst-first
        local gaps_file="$OUTPUT_DIR/coverage_gaps.txt"
        coverage report --show-missing 2>/dev/null | \
            grep -v "^-\|^Name\|^TOTAL\|^$\|100%" | \
            sort -t'%' -k1 -n > "$gaps_file" 2>/dev/null || true

        if [ ! -s "$gaps_file" ]; then
            echo "No coverage gaps found (100% coverage) or no data. Run 'coverage-wrapper run' first."
            return
        fi

        local line_count
        line_count=$(wc -l < "$gaps_file")

        if [ "$line_count" -le 40 ]; then
            echo "Files with missing coverage (worst first):"
            echo ""
            cat "$gaps_file"
        else
            echo "Files with missing coverage: $line_count files"
            echo "Written to: $gaps_file"
            echo ""
            echo "Worst 15 files:"
            head -15 "$gaps_file"
            echo ""
            echo "Use Read tool on $gaps_file for full list."
        fi
    fi
}

cmd_html() {
    coverage html 2>/dev/null || {
        echo "No coverage data. Run 'coverage-wrapper run' first."
        exit 1
    }
    echo "HTML report generated in htmlcov/"
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
    report)
        shift
        cmd_report "$@"
        ;;
    gaps)
        shift
        cmd_gaps "$@"
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
