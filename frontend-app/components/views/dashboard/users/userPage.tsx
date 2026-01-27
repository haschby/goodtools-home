// "use client";

// import { DataListProvider } from "@/components/providers/DataListProvider";
// import { getTotalRecordsByEntity } from "@/actions/common";
// import { getUsers } from "@/actions/users";
// import { configTable } from "./configTable";
// import { User } from "@/lib/types/user";

// import { useDataTable } from '@/lib/contexts/DataTableCustomContext';

// export default function UserPage() {
//     return (
//         <DataListProvider<User>
//             fetchTotalRowsFunction={getTotalRecordsByEntity}
//             statuses={configTable.statuses}
//             status={undefined}
//             fetchFunction={getUsers}
//             columns={ configTable.columns }
//             entity="user"
//         >
//             <UserListTitleInfo />
//         </DataListProvider>
//     );
// }


// export function UserListTitleInfo() {

//     const { totalRows } = useDataTable<User>();

//     const setBGcolorToRows = (length: unknown | number) => {
//         if (length === 0) return 'bg-slate-200 text-slate-500';
//         return 'bg-amber-300/20 text-amber-500';
//     }

//     return (
//         <div className="flex items-center justify-between w-full gap-2 px-6">
//             <h1 className="flex flex-col items-start text-2xl font-semibold text-gray-800">
//                 Users
//                 <span className={`my-2 text-xs rounded-md px-2 py-1 ${setBGcolorToRows(totalRows as number)}`}>
//                     <pre className="text-slate-800 inline-flex mr-3">Rows</pre>
//                     { totalRows as number }
//                 </span>
//             </h1>
//         </div>
//     );
// }