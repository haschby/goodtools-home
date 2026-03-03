import { ReactNode } from "react";
import UserIdLayout from "@/components/layouts/dashboard/user/UserIdLayout";

interface UsersPageIdLayoutProps {
    details: ReactNode;
    metrics: ReactNode;
}

export default function UsersPageIdLayout({ details, metrics }: UsersPageIdLayoutProps) {
    return (
        <UserIdLayout>
            {details}
            {metrics}
        </UserIdLayout>
    )
}