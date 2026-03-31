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
  paginationActions = <></>,
  statuses = undefined,
  data,
  headers,
  controlTableActions = undefined,
}: ListViewProps) {

  const listviewContainerRef = useRef<HTMLDivElement>(null);
  const [heightModulePixels, setHeightModulePixels] = useState<string>('');

  // ✅ Toujours à jour
  useEffect(() => {
    const windowHeight = window.innerHeight;
    const top = listviewContainerRef.current?.getBoundingClientRect().top;
    const availableHeight = windowHeight - (top || 0) - 57 - 12 + 15;
    setHeightModulePixels(`${Math.max(availableHeight, 0)}`);
  }, []);

  return (
    <>
      { !!statuses && <>{statuses}</> }
      { !!filters && <>{filters}</> }

      <div
        id="listview-container"
        ref={listviewContainerRef}
        style={{ height: `${parseInt(heightModulePixels)-100}px` }}
        className="relative w-full bg-white border-t border-r border-l border-gray-200 rounded-t-xl h-full overflow-hidden">
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
        { !!controlTableActions && <>{controlTableActions}</> }
      </div>
      { !!paginationActions && <>{paginationActions}</> }
      
      {/* <div className="bg-white p-4 rounded-b-xl border border-gray-200"> */}
      {/* </div> */}
    </>
  );
}