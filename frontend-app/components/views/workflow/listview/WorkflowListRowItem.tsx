"use client";

import { Workflow } from "@/lib/types/workflow";
import { RowItem } from "@/components/atoms/listview/RowItems/Row";
import { ColumnProps } from "@/lib/types/common";
import { workflowsColumns } from "@/components/views/workflow/config/config.columns";

interface WorkflowListRowItemProps {
    data: Workflow[];
}

export default function WorkflowListRowItem(
    { data }: WorkflowListRowItemProps
) {

    return (
        <>
            { 
                data.map(
                (workflow: Workflow, index: number) => {
                    return (
                        <tr
                            id={workflow.id}
                            key={`${workflow.id}-${index}`}
                            className="bg-white cursor-pointer border-b border-gray-100 text-gray-600 text-left">
                            {
                                workflowsColumns.map(
                                    (column: ColumnProps<Workflow>) =>
                                    <RowItem
                                        key={column.keyfield}
                                        isFirst={column.isFirst}
                                        isLast={column.isLast}
                                        maxWidth={column.maxWidth}
                                        isNumber={column.isNumber}
                                        renderItem={column.renderItem(workflow)}
                                    />
                                )}
                        </tr>
                    ) 
                }
            )}
        </>
    )
}