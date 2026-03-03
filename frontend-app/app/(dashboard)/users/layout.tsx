import UserLayout from "@/components/layouts/dashboard/user/UserLayout";

export default function UsersLayout({ children }: { children: React.ReactNode }) {
    return (
        <UserLayout>
            {children}
        </UserLayout>
    )
}