# Modern React Patterns & Performance

This guide covers advanced patterns for building scalable, performant React applications in the era of React 18+ and Server Components.

## 1. Composition over Inheritance

React favors composition. Don't build massive "God Components" with 50 props.

### Pattern: Compound Components
Allow users to compose UI parts flexibly.

```tsx
// ❌ Bad: One giant component
<Select options={opts} onChange={fn} label="Foo" />

// ✅ Good: Compound Components
<Select.Root onChange={fn}>
  <Select.Label>Foo</Select.Label>
  <Select.Trigger />
  <Select.Content>
    {opts.map(o => <Select.Item key={o.id} value={o.value} />)}
  </Select.Content>
</Select.Root>
```

### Pattern: Render Props / Function as Child
Useful for "Headless" logic (though Custom Hooks usually prefered now).

```tsx
<MouseTracker>
  {(x, y) => <p>Mouse is at {x}, {y}</p>}
</MouseTracker>
```

## 2. State Management Rules

### Server State (Async)
**Tool:** TanStack Query (React Query).
**Rule:** NEVER put API data in `useEffect` + `useState`. It handles caching, deduping, loading, error, retries.

```tsx
// ✅ Correct
const { data, isLoading } = useQuery({ queryKey: ['todos'], queryFn: fetchTodos });
```

### Client State (Global)
**Tool:** Zustand.
**Rule:** Use for "Session" state (Sidebar open, Theme, User Preferences).
**Avoid:** Redux (too much boilerplate for most apps). Context (Re-renders *everything* unless split carefully).

### Derived State
**Rule:** If you can calculate it from props/state, DO NOT put it in state.

```tsx
// ❌ Bad
const [total, setTotal] = useState(0);
useEffect(() => setTotal(a + b), [a, b]);

// ✅ Good
const total = a + b;
```

## 3. Performance Optimization

### The "Render" Cycle
React re-renders a component when:
1.  Props change.
2.  State changes.
3.  Parent re-renders.

### Memoization (`useMemo`, `useCallback`)
*   **Don't Prematurely Memoize:** It has a cost.
*   **Do Memoize When:**
    1.  Passing a function/object as a prop to a `React.memo` wrapped child.
    2.  Passing a function/object to a `useEffect` dependency array.
    3.  Calculating "Expensive" things (array sorting, massive filtering).

### Code Splitting (Lazy Loading)
Split bundles to improve initial load (LCP).

```tsx
const HeavyChart = lazy(() => import('./HeavyChart'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <HeavyChart />
    </Suspense>
  );
}
```

## 4. Custom Hooks Logic

Extract logic from view.

```tsx
// components/UserList.tsx
function UserList() {
  // Logic extracted to hook
  const { users, sort, setSort } = useUsersList(); 
  
  return (
    <div>
       {/* Pure JSX - no complex logic here */}
    </div>
  )
}
```

## 5. Directory Structure (Feature-Based)

Don't group by file type. Group by Feature.

```
src/
  features/
    auth/
      components/
      hooks/
      api.ts
    dashboard/
      components/
      hooks/
```
