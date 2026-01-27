"use client";
import { ComponentType, SVGProps,  } from "react";
import { Lineicons } from "@lineiconshq/react-lineicons";

interface IconData {
    svg: string;
    viewBox: string;
    hasFill: boolean;
    hasStroke: boolean;
    hasStrokeWidth: boolean;
}

interface IconProps {
    Icon: ComponentType<SVGProps<SVGSVGElement>> & IconData;
    size?: number | string;
    color?: string;
    strokeWidth?: number;
    className?: string;
}

export default function Icon({ Icon, size, strokeWidth, className }: IconProps) {
    return (
        <Lineicons
            icon={Icon}
            size={size}
            strokeWidth={strokeWidth}
            className={className}
        />
    );
}