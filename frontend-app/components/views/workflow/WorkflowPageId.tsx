"use client";
import { useEffect, useState } from "react";
import { useParams} from "next/navigation";
import Link from "next/link";
import { pollWorkflow } from "@/actions/workflow";
import { ListView } from "@/components/atoms/listview/ListView";
import { RowItem } from '@/components/atoms/listview/RowItems/Row';  
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";
import Icon from "@/components/atoms/Icon";
import { ArrowLeftDuotone, Bell1Solid, PartySpraySolid, WaterDrop1Duotone } from '@lineiconshq/free-icons';

interface Params {
    [key: string]: string | number | boolean | object | null;
}

interface Workflow {
    status: 'Not Started' | 'Processing' | 'Completed' | 'Failed' | 'Skipped' | 'Aborted' | 'Pending';
    provider: string;
    ref_pulling: string;
    created_at: string;
    ended_at: string;
    params: Params;
    steps: Workflow_Step[];
    message: string;
}

interface Workflow_Step {
    name: string;
    status: string;
    ended_at: string;
    updated_at: string;
    params: Params;
    message: string;
}

export default function WorkflowPageId() {

    const { provider, id } = useParams();
    const [workflow, setWorkflow] = useState<Workflow|null>(null);

    useEffect(() => {
        const fetchWorkflow = async () => {
            const workflow = await pollWorkflow({ id: `${id}` }) as unknown as Workflow;
            setWorkflow(workflow as unknown as Workflow);
            if (workflow?.status !== 'Pending') {
                clearInterval(interval);
            }
        }
        fetchWorkflow();
        const interval = setInterval(fetchWorkflow, 4000);
        return () => clearInterval(interval);
    }, [id]);

    return (
        <div className="h-screen bg-gray-50">
            <div className="flex flex-col h-full text-gray-700 gap-2 w-full">

                <aside className="flex flex-col items-start w-full">
                    <div className="p-6 flex flex-col w-full">
                        <h1 className="flex items-center text-2xl font-semibold text-gray-800 gap-4">
                            <Link
                                title="Back to workflows"
                                href={`/workflows`}
                                className="shadow-sm bg-white rounded-sm p-1 border border-gray-200 inline-flex items-center gap-2">
                                <Icon Icon={ArrowLeftDuotone} size={20} strokeWidth={2} />
                            </Link>
                            Workflow Id: 
                            {
                                workflow?.ref_pulling && (
                                    <span className="text-sm text-purple-400 bg-purple-200 rounded-sm p-1 border border-purple-300 font-semibold">
                                        #{`${workflow?.ref_pulling || 'N/A'}`.toUpperCase()}
                                    </span>
                                )
                            }
                        </h1>
                        <p className="text-xs text-gray-400 ml-12">
                            Detailed workflow information by provider.
                        </p>
                    </div>
                </aside>

                <aside className="flex flex-col items-start w-full px-6">
                    <p className="self-start self-start flex flex-col gap-2">                        
                        <StatusRow className="px-2 py-1 text-lg" status={`${workflow?.status}`} />
                    </p>
                </aside>

                <aside className="flex flex-col items-start w-full px-6">
                    { workflow?.message && workflow?.status !== 'Completed' && (
                        <p className="self-start bg-red-400/10 text-red-800/80 border border-red-200 rounded-md p-2 self-start flex flex-col gap-2">
                            <span className="text-md font-semibold">
                                Alerting Message
                            </span>
                            {`${workflow?.message !== null && workflow?.message || 'N/A' }`}  
                        </p>
                    )}
                </aside>

                <aside className="flex flex-col items-start w-full px-6">
                    <div className="bg-white border border-gray-100 rounded-md p-4 text-xs text-gray-500 flex flex-col items-start gap-2 w-full max-w-md">
                        <p className="flex flex-row items-center justify-between w-full">
                            <span className="font-semibold">Started at</span>
                            {`${workflow?.created_at !== null && workflow?.created_at || 'N/A' }`}  
                        </p>
                        <p className="flex flex-row items-center justify-between w-full">
                            <span className="font-semibold">Ended at</span>
                            {`${workflow?.ended_at !== null && workflow?.ended_at || 'N/A' }`}  
                        </p>
                    </div>
                </aside>

                <aside className="flex flex-row w-full">                
                    <ListView
                        data={
                            workflow?.steps?.map(
                                (step: Workflow_Step, index: number) => 
                                (
                                    <tr key={index} className="bg-white cursor-pointer border-b border-gray-100 text-gray-600 text-left">
                                        <RowItem
                                            renderItem={
                                                <span className="text-sm font-semibold">{`${step.name}`}</span>
                                            }
                                        />
                                        <RowItem
                                            renderItem={
                                                <StatusRow className="px-2 py-1 text-xs" status={`${step.status}`} />
                                            }
                                        />
                                        <RowItem
                                            renderItem={
                                                <span className="text-sm font-semibold">{`${step.ended_at !== null && step.ended_at || 'N/A' }`}</span>
                                            }
                                        />
                                        <RowItem
                                            renderItem={
                                                <span className="text-sm font-semibold">{`${step.message !== null && step.message || 'N/A' }`}</span>
                                            }
                                        />
                                    </tr>
                                )
                            )
                        }
                        headers={<Headers />}
                        statuses={<></>}
                        filters={<></>}
                        actionsList={<></>}
                    />
                    <div className="w-5/6 bg-white border border-gray-200 p-6 flex flex-col gap-4">
                        <h2 className="text-lg font-semibold">
                            <Icon
                                Icon={PartySpraySolid}
                                size={20}
                                strokeWidth={2}
                                className="inline-block mr-2"
                            />
                            Workflow Parameters
                        </h2>
                        <pre className="text-sm text-gray-200 bg-gray-800 p-4 rounded-md overflow-y-scroll min-h-[600px] max-h-[600px]">
                            {JSON.stringify(workflow?.params, null, 1)}
                        </pre>
                    </div>
                </aside>

            </div>
        </div>
    );
}

const Headers = () => {
    return (
    <>
        <th key={0} style={{ width: '350px' }} className="bg-amber-50/50 whitespace-nowrap text-sm font-bold">
            <span className="px-6 border-r border-t border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                {'Job Name'} 
            </span>
        </th>
        <th key={1} style={{ width: '180px' }} className="bg-amber-50/50 whitespace-nowrap text-sm font-bold">
            <span className="px-6 border-r border-t border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                {'Job Status'} 
            </span>
        </th>
        <th key={2} style={{ width: '200px' }} className="bg-amber-50/50 whitespace-nowrap text-sm font-bold">
            <span className="px-6 border-r border-t border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                {'Ended At'} 
            </span>
        </th>
        <th key={3} style={{ width: '300px' }} className="bg-amber-50/50 whitespace-nowrap text-sm font-bold">
            <span className="px-6 border-r border-t border-gray-50 pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200">
                {'Message'} 
            </span>
        </th>
    </>
    )
}
    /*return (
        <div className="flex flex-col h-full text-gray-700 gap-4 w-full">

            <aside className="flex flex-col items-start gap-6 pt-8 px-8">
                <p className="text-gray-700 font-semibold">
                    <Link href={`/workflows`}>
                        <Icon
                            Icon={ArrowLeftDuotone}
                            size={20}
                            strokeWidth={2}
                            className="inline-block text-gray-800 mr-2"
                        />
                        Workflows
                    </Link>/
                    <Link href={`/workflows/${provider}`}
                    className="underline">
                        {`${workflow?.provider}`}
                    </Link>/
                </p>
                <p className="flex items-center gap-2">
                    {
                        workflow?.status === 'Pending' && (
                            <Icon 
                                Icon={Bell1Solid}
                                size={20}
                                strokeWidth={2}
                                className="text-green-600 animate-spin"
                            />
                        )
                    }
                    <StatusRow
                        className="px-3 py-2 text-xl"
                        status={`${workflow?.status || 'Not Started'}`} />
                    JOBID: 
                    <span
                        className="ml-1 text-purple-400 bg-purple-200 rounded-sm p-1 border border-purple-300 font-semibold">
                        {`${workflow?.ref_pulling}`.toUpperCase()}
                    </span>
                </p>


                { workflow?.message && workflow?.status !== 'Completed' && (
                    <p className="self-start bg-red-400/10 text-red-800/80 border border-red-200 rounded-md p-2 self-start flex flex-col gap-2">
                        <span className="text-md font-semibold">
                            Alerting Message
                        </span>
                        {`${workflow?.message !== null && workflow?.message || 'N/A' }`}  
                    </p>
                )}
                
            
            </aside>
            <section className="flex flex-row gap-4 px-8">
                <aside className="bg-white border border-gray-100 rounded-md p-4 text-xs text-gray-500 flex flex-col items-start gap-2 w-full max-w-md">
                    <p className="flex flex-row items-center justify-between w-full">
                        <span className="font-semibold">Started at</span>
                        {`${workflow?.created_at !== null && workflow?.created_at || 'N/A' }`}  
                    </p>
                    <p className="flex flex-row items-center justify-between w-full">
                        <span className="font-semibold">Ended at</span>
                        {`${workflow?.ended_at !== null && workflow?.ended_at || 'N/A' }`}  
                    </p>
                </aside>
            </section>
            
            <aside className="flex flex-row w-full">                
                <ListView
                    data={
                        workflow?.steps?.map(
                            (step: Workflow_Step, index: number) => 
                            (
                                <tr key={index} className="bg-white cursor-pointer border-b border-gray-100 text-gray-600 text-left">
                                    <RowItem
                                        renderItem={
                                            <span className="text-sm font-semibold">{`${step.name}`}</span>
                                        }
                                    />
                                    <RowItem
                                        renderItem={
                                            <StatusRow className="px-2 py-1 text-xs" status={`${step.status}`} />
                                        }
                                    />
                                    <RowItem
                                        renderItem={
                                            <span className="text-sm font-semibold">{`${step.ended_at !== null && step.ended_at || 'N/A' }`}</span>
                                        }
                                    />
                                    <RowItem
                                        renderItem={
                                            <span className="text-sm font-semibold">{`${step.message !== null && step.message || 'N/A' }`}</span>
                                        }
                                    />
                                </tr>
                            )
                        )
                    }
                    headers={<Headers />}
                    statuses={<></>}
                    filters={<></>}
                    actionsList={<></>}
                />
            </aside>
        </div>  
    )
}*/

