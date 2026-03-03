import { useRef, useCallback } from "react";

export function useDebouncedCallback<T extends unknown[]>(
  callback: (...args: T) => void,
  delay: number
) {
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const debouncedFn = useCallback(
    (...args: T) => {
      // annuler le timeout précédent
      if (timerRef.current) clearTimeout(timerRef.current);

      timerRef.current = setTimeout(() => {
        callback(...args);
      }, delay);
    },
    [callback, delay]
  );

  return debouncedFn;
}