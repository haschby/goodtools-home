import { startWorkflow } from "@/actions/workflow";
import Icon from "@/components/atoms/Icon";
import { Cloud2Stroke } from "@lineiconshq/free-icons";
import { useRouter } from "next/navigation";

export default function InvoicePennylaneAction() {
    
    const router = useRouter();

    const handleSync = async () => {
        const uniqueId = Math.random().toString(36).substring(2, 15);
        const provider = "pennylane";
        await startWorkflow({ provider, id: uniqueId, workflowName: 'syncPennyLaneWorkflow' });
        router.push(`/workflows/${provider}/sync/${uniqueId}`);
    }

    return (
        <button
            className="self-end bg-green-500 text-white group cursor-pointer py-2 px-4 rounded-md border border-green-600"
            onClick={handleSync}>
            <span className="text-xs flex items-center gap-2 font-semibold">
                <Icon
                    Icon={Cloud2Stroke}
                    size={16}
                    strokeWidth={3}
                    className="" />
                Pennylane Sync
            </span>
        </button>
    )
}