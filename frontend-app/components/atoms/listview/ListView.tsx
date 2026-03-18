"use client";

import { ReactNode, useEffect, useRef, useState, useCallback } from 'react';

interface ListViewProps {
  statuses?: ReactNode | undefined;
  filters?: ReactNode | undefined;
  data?: ReactNode | undefined;
  actionsList?: ReactNode | undefined;
  headers?: ReactNode | undefined;
  controlTableActions?: ReactNode | undefined;
  onScrollEnd?: (isEndOfList: boolean) => void;
}

export function ListView({
  filters = <></>,
  actionsList = <></>,
  statuses = undefined,
  data,
  headers,
  controlTableActions = undefined,
  onScrollEnd = () => {}
}: ListViewProps) {

  const listviewContainerRef = useRef<HTMLDivElement>(null);
  const savedScrollTopRef = useRef<number>(0);
  const [heightModulePixels, setHeightModulePixels] = useState<string>('');
  const onScrollEndRef = useRef(onScrollEnd);

  // ✅ Toujours à jour
  useEffect(() => {
    onScrollEndRef.current = onScrollEnd;
  }, [onScrollEnd]);

  const handleResize = useCallback(() => {
    requestAnimationFrame(() => {
      const container = listviewContainerRef.current;
      if (!container) return;
      container.style.height = 'auto';
      requestAnimationFrame(() => {
        const { top } = container.getBoundingClientRect();
        const availableHeight = window.innerHeight - top - 57 - 12 + 15;
        container.style.height = `${Math.max(availableHeight, 200)}px`;
        setHeightModulePixels(`${Math.max(availableHeight, 200)}`);
      });
    });
  }, []);

  const scrollToBottom = useCallback((e: Event) => {
    const container = e.target as HTMLDivElement;
    const { scrollTop, scrollHeight, clientHeight } = container;
    const pourcentage = Math.round((scrollTop / (scrollHeight - clientHeight)) * 100);

    if (pourcentage === 100) {
      savedScrollTopRef.current = scrollTop; // ✅ sauvegarde

      const tbody = container.querySelector('tbody');
      if (!tbody) return;

      const observer = new MutationObserver(() => {
        const newScrollHeight = container.scrollHeight;
        if (newScrollHeight <= scrollHeight) return; // attend que les nouvelles lignes soient là

        container.scrollTop = savedScrollTopRef.current; // ✅ restaure
        observer.disconnect();
      });

      observer.observe(tbody, { childList: true, subtree: true });
      onScrollEndRef.current(true); // ✅ appelé une seule fois
    }
  }, []);

  useEffect(() => {
    const container = listviewContainerRef.current;
    if (!container) return;

    handleResize();
    container.addEventListener('scroll', scrollToBottom);
    window.addEventListener('resize', handleResize, { passive: true });

    return () => {
      container.removeEventListener('scroll', scrollToBottom);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <>
      { !!statuses && <>{statuses}</> }
      { !!filters && <>{filters}</> }
      { !!actionsList && <>{actionsList}</> }

      <div
        id="listview-container"
        ref={listviewContainerRef}
        style={{ height: `${heightModulePixels}px` }}
        className="w-full bg-white overflow-x-scroll overflow-y-scroll overflow-hidden border-b border-gray-200">
        <table className="table-fixed border-collapse w-full">
          <thead className="w-full sticky top-0 left-0 right-0 z-50">
            <tr className="bg-green-50">
              {headers}
            </tr>
          </thead>
          <tbody>
            {data}
          </tbody>
        </table>
      </div>
      { !!controlTableActions && <>{controlTableActions}</> }
    </>
  );
}