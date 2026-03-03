export interface Workflow {
    id: string;
    name: string;
    status: string;
    provider: string;
    created_at: string;
    ended_at: string;
    steps: Workflow_Step[];
}

export interface Workflow_Step {
    name: string;
    status: string;
    ended_at: string;
    updated_at: string;
}