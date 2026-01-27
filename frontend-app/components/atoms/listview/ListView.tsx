"use client";

import { ReactNode, useEffect, useRef } from 'react';

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
  const scrollTopRef = useRef<number>(0);

  useEffect(() => {
    const el = listviewContainerRef.current;
    if (!el) return;

    requestAnimationFrame(() => {
      el.scrollTop = scrollTopRef.current;
    });
  }, [data]);

  useEffect(() => {  
    const el = listviewContainerRef.current;
    if (!el) return;

    const handleScroll = (e: Event) => {
      const { 
        scrollTop, scrollHeight, 
        clientHeight, scrollLeft } = e.target as HTMLDivElement;

      if (scrollLeft > 0) {
        return;
      }

      scrollTopRef.current = scrollTop;
      if (
        scrollTop > 0 &&
        (scrollTop + clientHeight >= scrollHeight)
      ) {

        onScrollEnd(true);
      }
    }

    el.addEventListener('scroll', handleScroll);

    return () => {
      el.removeEventListener('scroll', handleScroll);
    }
  }, [listviewContainerRef, onScrollEnd]);

  return (
    <>
      { !!statuses && <>{statuses}</> }
      { !!filters && <>{filters}</> }
      { !!actionsList && <>{actionsList}</> }
      {/* TABLE */}
      <div
        ref={listviewContainerRef}
        className="w-full h-[calc(-310px+100vh)] bg-white overflow-x-scroll overflow-y-scroll overflow-hidden border-b border-gray-200">
        <table className="table-fixed w-full border-collapse">
          <thead className="w-full sticky top-0 left-0 right-0 z-50">
            <tr className="bg-gray-100 text-gray-700">
              {headers}
            </tr>
          </thead>
          <tbody> 
            {data}
          </tbody>
        </table>
        {controlTableActions}
      </div>
    </>
  );
}