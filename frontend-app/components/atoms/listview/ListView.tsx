"use client";

import { ReactNode, useEffect, useRef, useState } from 'react';

interface ListViewProps {
  statuses?: ReactNode | undefined;
  filters?: ReactNode | undefined;
  data?: ReactNode | undefined;
  paginationActions?: ReactNode | undefined;
  headers?: ReactNode | undefined;
  controlTableActions?: ReactNode | undefined;
}

export function ListView({
  filters = <></>,
  paginationActions = undefined,
  statuses = undefined,
  data,
  headers,
  controlTableActions = undefined,
}: ListViewProps) {

  const listviewContainerRef = useRef<HTMLDivElement>(null);
  const controlTableActionsRef = useRef<HTMLDivElement>(null);
  const [heightModulePixels, setHeightModulePixels] = useState<number>(0);
  const [controlTableActionsHeight, setControlTableActionsHeight] = useState<number>(0);

  useEffect(() => {
    const computeHeight = () => {
      const windowHeight = window.innerHeight;
      const top = listviewContainerRef.current?.getBoundingClientRect().top;
      const availableHeight = windowHeight - (top || 0) - 57 - 12 + 15;
      setHeightModulePixels(Math.max(availableHeight, 0));
    };

    computeHeight();

    const resizeObserver = new ResizeObserver(() => computeHeight());
    resizeObserver.observe(document.body);

    return () => resizeObserver.disconnect();
  }, []);

  useEffect(() => {
    const element = controlTableActionsRef.current;
    if (!element) {
      setControlTableActionsHeight(0);
      return;
    }

    const controlObserver = new ResizeObserver(() => {
      setControlTableActionsHeight(element.getBoundingClientRect().height);
    });
    controlObserver.observe(element);

    return () => controlObserver.disconnect();
  }, [controlTableActions]);

  const cssHeader = paginationActions ? undefined :'border-b rounded-b-xl';

  return (
    <>
      { !!statuses && <>{statuses}</> }
      { !!filters && <>{filters}</> }
      <div
        id="listview-container"
        ref={listviewContainerRef}
        style={{ height: `${heightModulePixels - 100 - controlTableActionsHeight}px` }}
        className={`${cssHeader ? cssHeader : ''} border-t relative bg-white border-gray-200 h-full overflow-hidden`}>
          <div className="overflow-x-scroll overflow-y-scroll overflow-hidden h-full"> 
            <table className="table-fixed border-collapse w-full">
              <thead className="w-full sticky top-0 left-0 right-0 z-50">
                <tr className="bg-white">
                  {headers}
                </tr>
              </thead>
              <tbody>
                {data}
              </tbody>
            </table>
          </div>
      </div>
      { !!paginationActions && <>{paginationActions}</> }
      { !!controlTableActions && <div ref={controlTableActionsRef}>{controlTableActions}</div> }
      
      {/* <div className="bg-white p-4 rounded-b-xl border border-gray-200"> */}
      {/* </div> */}
    </>
  );
}