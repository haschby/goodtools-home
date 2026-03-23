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
                            className="cursor-pointer hover:bg-green-300/20 transition-all duration-300">
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