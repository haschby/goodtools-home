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
  const onScrollEndRef = useRef(onScrollEnd);

  useEffect(() => {
    onScrollEndRef.current = onScrollEnd;
  }, [onScrollEnd]);

  useEffect(() => {  
    console.log('ListView useEffect');
    const el = listviewContainerRef.current;
    if (!el) return;
    const tbody = el.querySelector('tbody');

    const handleScroll = (e: Event) => {
      console.log('ListView useEffect handleScroll');
      const { scrollTop, scrollHeight, clientHeight, scrollLeft } = e.target as HTMLDivElement;
      if (scrollLeft > 0) return;

      scrollTopRef.current = scrollTop;

      if (scrollTop > 0 && scrollTop + clientHeight + 1 >= scrollHeight) {
        const savedScrollTop = scrollTop;
        const savedScrollHeight = scrollHeight;
        console.log('SCROLL END — savedScrollTop:', savedScrollTop, 'savedScrollHeight:', savedScrollHeight);

        // ✅ Observer qui se déclenche quand React injecte les nouvelles lignes
        const observer = new MutationObserver(() => {
          console.log('MUTATION — newScrollHeight:', el.scrollHeight, 'addedHeight:', el.scrollHeight - savedScrollHeight);
          const newScrollHeight = el.scrollHeight;
          const addedHeight = newScrollHeight - savedScrollHeight;
          if (addedHeight > 0) {  
            el.scrollTop = savedScrollTop + addedHeight;
            console.log('RESTORED scrollTop to:', el.scrollTop);
          }
          observer.disconnect(); // ✅ one-shot
        });

        if (tbody) {
            observer.observe(tbody, { childList: true, subtree: true });
        }

        onScrollEndRef.current(true);
      }
    };

    el.addEventListener('scroll', handleScroll);
    return () => el.removeEventListener('scroll', handleScroll);
  }, [])

  function handleResize() {
    const el = listviewContainerRef.current;
    if (!el) return;
    const windowHeight = window.innerHeight;
    const topTable = el.getBoundingClientRect().top;
    const heightListView = windowHeight - (topTable + 200);
    heightModulePixels.current = window.innerHeight - 269;
    if (heightListView > 0) {
      el.style.height = `${heightListView}px`;
    }
  }

  useEffect(() => {
    const el = listviewContainerRef.current;
    if (!el) return;

    handleResize();
    el.addEventListener('resize', handleResize);
    return () => el.removeEventListener('resize', handleResize);
  }, []);


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