// import { ReactNode, createContext, useState } from "react";


// const GenericFormContext = createContext<GenericFormContextType>({});

// interface GenericFormContextType {
//     [key: string]: unknown;
// }

// interface AddFieldProps {
//     field: string;
//     value: unknown;
// }

// interface GenericFormProviderProps {
//     children: ReactNode;
//     initialFields: { [key: string]: string };
// }

// export function GenericFormProvider(
//     { children, initialFields }: GenericFormProviderProps
// ) {

//     const contextValue: GenericFormContextType = {
//         initialFields,
//         changeFieldValue: ({field, value}: AddFieldProps) => {
            
//         },
//     };

//     return (
//         <GenericFormContext.Provider
//         value={{}}>
//             {children}
//         </GenericFormContext.Provider>
//     )
// }