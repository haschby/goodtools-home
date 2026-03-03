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
  const heightModulePixels = useRef<number>(0);

  useEffect(
    () => {  
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
        (scrollTop + clientHeight + 1 >= scrollHeight)
      ) {
        onScrollEnd(true);
      }
    }

    el.addEventListener('scroll', handleScroll);
    return () => {
      el.removeEventListener('scroll', handleScroll);
    }
  }, [listviewContainerRef, onScrollEnd]);

  function handleResize() {
    const el = listviewContainerRef.current;
    if (!el) return;
    const windowHeight = window.innerHeight;
    const topTable = el.getBoundingClientRect().top;
    const heightListView = windowHeight - (topTable + 200);
    heightModulePixels.current = window.innerHeight-269;
    if (heightListView > 0) {
      el.style.height = `${heightListView}px`;
    }
  }

  useEffect(() => {
    const el = listviewContainerRef.current;
    if (!el) return;

    handleResize();
    el.addEventListener('resize', handleResize);
    return () => {
      el.removeEventListener('resize', handleResize);
    }
  }, [listviewContainerRef]);


  return (
    <>
      {/* {setHeightListView} */}

      { !!statuses && <>{statuses}</> }
      { !!filters && <>{filters}</> }
      { !!actionsList && <>{actionsList}</> }

      {/* TABLE */}
      <div
        id="listview-container"
        ref={listviewContainerRef}
        style={{ height: `${heightModulePixels.current}px` }}
        className="w-full bg-white overflow-x-scroll overflow-y-scroll overflow-hidden border-b border-gray-200">
        <table className="table-fixed border-collapse w-full">
          <thead className="w-full sticky top-0 left-0 right-0 z-50">
            <tr className="bg-gray-100 text-gray-700">
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