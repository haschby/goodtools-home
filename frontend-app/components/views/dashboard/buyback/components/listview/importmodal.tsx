"use client";

import { ChangeEvent, useRef, useState } from "react";
import Icon from "@/components/atoms/Icon";
import { PlusStroke } from "@lineiconshq/free-icons";
import { Buyback } from "@/lib/types/buyback";
import { createBuybacks } from "@/actions/buyback.action";

type FileStatus = "loading" | "ready" | "error";

type FileItem = {
    id: string;
    file: File;
    status: FileStatus;
    progress: number;
    fileSize: { size: number; unit: string };
    fileExtension: string;
};

const ACCEPTED_TYPES = "image/jpeg,image/png,image/gif,application/pdf";

function formatFileSize(bytes: number) {
    const units = ["B", "KB", "MB", "GB"];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return {
        size: Number(size.toFixed(2)),
        unit: units[unitIndex],
    };
}

interface BuybackImportModalProps {
    onClose: () => void;
    refreshTable: () => void;
}

export function BuybackImportModal({ onClose, refreshTable }: BuybackImportModalProps) {
    const inputRef = useRef<HTMLInputElement>(null);
    const [files, setFiles] = useState<FileItem[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleImportFile = () => {
        inputRef.current?.click();
    };

    const updateFile = (id: string, patch: Partial<FileItem>) => {
        setFiles((prev) =>
            prev.map(
                (item) =>
                (item.id === id ? { ...item, ...patch } : item)
            )
        );
    };

    // Chargement progressif visuel pendant la lecture locale du fichier.
    const startProgressiveLoad = (id: string) => {
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 20;
            if (progress >= 100) {
                clearInterval(interval);
                updateFile(id, { progress: 100, status: "ready" });
            } else {
                updateFile(id, { progress: Math.round(progress) });
            }
        }, 200);
    };

    const handleChangeFile = (event: ChangeEvent<HTMLInputElement>) => {
        const selected = event.target.files;
        if (!selected) return;

        const newItems: FileItem[] = Array.from(selected).map((file) => ({
            id: `${file.name}-${file.size}-${crypto.randomUUID()}`,
            file,
            status: "loading",
            progress: 0,
            fileSize: formatFileSize(file.size),
            fileExtension: file.name.split(".").pop() ?? "",
        }));

        setFiles((prev) => [...prev, ...newItems]);
        newItems.forEach((item) => startProgressiveLoad(item.id));

        event.target.value = "";
    };

    const removeFile = (id: string) => {
        setFiles((prev) => prev.filter((item) => item.id !== id));
    };

    const allReady = files.length > 0 && files.every((item) => item.status === "ready");

    const handleValidate = async () => {
        if (!allReady || isSubmitting) return;
        setIsSubmitting(true);
        setError(null);

        try {
            const formData = new FormData();
            files.forEach((item) => formData.append("files", item.file));

            const response = await createBuybacks(formData);
            if (response.status_code !== 201 || !response.data) {
                throw new Error(response.message ?? "Échec de la création des buybacks");
            }

            refreshTable();
            onClose();
        } catch (err) {
            console.log("err", err);
            setError(String(err));
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 z-9999 flex items-center justify-center bg-black/40 p-4">
            <div className="flex max-h-[80vh] w-full max-w-2xl flex-col gap-4 overflow-hidden rounded-xl bg-white p-6 shadow-xl">
                <div className="flex items-center justify-between">
                    <h2 className="text-lg font-bold text-gray-800">Importer des tickets</h2>
                    <button
                        onClick={onClose}
                        className="text-gray-400 transition-colors hover:text-gray-700">
                        ✕
                    </button>
                </div>

                <input
                    ref={inputRef}
                    type="file"
                    multiple
                    accept={ACCEPTED_TYPES}
                    onChange={handleChangeFile}
                    className="hidden"
                />

                <button
                    onClick={handleImportFile}
                    className="flex items-center justify-center gap-2 rounded-lg border-2 border-dashed border-gray-300 px-4 py-6 text-gray-500 transition-colors hover:border-blue-400 hover:text-blue-500">
                    <Icon Icon={PlusStroke} size={18} strokeWidth={2} />
                    <span className="text-sm">Ajouter des fichiers</span>
                </button>

                <div className="flex flex-col gap-2 overflow-y-auto">
                    {files.length === 0 && (
                        <p className="text-center text-sm text-gray-400">Aucun fichier ajouté</p>
                    )}
                    {files.map((item) => (
                        <div
                            key={item.id}
                            className="flex flex-col gap-1 rounded-md border border-gray-200 bg-white p-2">
                            <div className="flex items-center justify-between gap-2">
                                <div className="flex min-w-0 flex-col">
                                    <p className="truncate text-sm font-semibold text-gray-700">
                                        {item.file.name}
                                    </p>
                                    <p className="flex gap-2 text-xs text-gray-500">
                                        <span>
                                            {item.fileSize.size} {item.fileSize.unit}
                                        </span>
                                        <span className="uppercase">{item.fileExtension}</span>
                                    </p>
                                </div>
                                <button
                                    onClick={() => removeFile(item.id)}
                                    disabled={isSubmitting}
                                    className="text-xs text-gray-400 hover:text-red-500 disabled:opacity-50">
                                    ✕
                                </button>
                            </div>

                            <div className="h-1.5 w-full overflow-hidden rounded-full bg-gray-100">
                                <div
                                    className={`h-full rounded-full transition-all duration-200 ${
                                        item.status === "error"
                                            ? "bg-red-500"
                                            : item.status === "ready"
                                            ? "bg-green-500"
                                            : "bg-blue-500"
                                    }`}
                                    style={{ width: `${item.progress}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>

                {error && <p className="text-sm text-red-500">{error}</p>}

                <div className="flex items-center justify-end gap-2 border-t border-gray-100 pt-4">
                    <button
                        onClick={onClose}
                        disabled={isSubmitting}
                        className="rounded-lg px-4 py-2 text-sm text-gray-600 transition-colors hover:bg-gray-100 disabled:opacity-50">
                        Annuler
                    </button>
                    <button
                        onClick={handleValidate}
                        disabled={!allReady || isSubmitting}
                        className="rounded-lg bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-50">
                        {isSubmitting ? "Validation..." : "Valider"}
                    </button>
                </div>
            </div>
        </div>
    );
}
