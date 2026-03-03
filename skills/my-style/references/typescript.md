# TypeScript-Specific Standards

Use alongside the core `my-style` skill. Formatting (line length, indentation, semicolons, quotes, trailing commas) is enforced by Prettier — not repeated here.

## Import Organization

1. React and related imports first
2. Standard library / external package imports
3. Local module imports (most global → most local, alphabetical within tier)

```typescript
import { useRef } from 'react';
import { useReducedMotion, useScroll } from 'framer-motion';
import { ParticleField } from '@/components';
import { projects } from '@/data/projects';
import { SECTION_HEIGHT_VH } from './animationConfig';
import { ParallaxCard } from './ParallaxCard';
import { ProjectCard } from './ProjectCard';
import type { Project } from './types';
```

## Arrow Functions (Preferred)

All functions should use arrow function syntax for consistency:

```typescript
const calculateTotal = (values: number[]): number => {
  return values.reduce((a, b) => a + b, 0);
};

// React components
const ExerciseCard: React.FC<ExerciseCardProps> = ({ exercise, onSubmit }) => {
  const [quantity, setQuantity] = useState(0);

  const handleSubmit = () => {
    onSubmit(quantity);
  };

  return (
    <div className="exercise-card">
      <h3>{exercise.name}</h3>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
};
```

**Exceptions — use regular functions only for:**

- Generator functions (`function*`)
- The rare case where hoisting is genuinely needed (usually a code smell)

## Named Exports

Always use named exports for React development.

## Absolute Imports

Always use absolute imports. Configure Vite to prefix `src` subdirectories with `@`:

```json
// tsconfig.app.json
{
  "compilerOptions": {
    "baseUrl": "src",
    "paths": {
      "@/*": ["*"]
    }
  }
}
```

```typescript
// ✅ Preferred
import type { Project } from '@/types';

// ❌ Avoid
import type { Project } from '../../types';
```