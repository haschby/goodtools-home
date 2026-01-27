// "use client";

// import { useRef, useState } from "react";
// import { uploadPdf } from "@/actions/ocr";

// interface UploadPdfResponse extends Response {
//     images: string[];
//     message: string;
//     result: unknown;
// }

// function base64ToBlob(
//     base64: string,
//     mimeType: string = "application/pdf"
// ): Blob {
//     const byteCharacters = atob(base64);
//     const byteNumbers = new Array(byteCharacters.length);
//     for (let i = 0; i < byteCharacters.length; i++) {
//         byteNumbers[i] = byteCharacters.charCodeAt(i);
//     }
//     const byteArray = new Uint8Array(byteNumbers);
//     return new Blob([byteArray], { type: mimeType });
// }

// function drawBoxes(
//     ctx: CanvasRenderingContext2D,
//     lines: { words: { geometry: [[number, number], [number, number]] }[] }[],
//     canvas: HTMLCanvasElement
// ) {
//     ctx.strokeStyle = "blue";
//     ctx.lineWidth = 1.5;
//     lines.forEach(
//         (line) => {
//             line.words.forEach(
//                 (word: { geometry: [[number, number], [number, number]] }) => {
//                     const [[xMin, yMin], [xMax, yMax]] = word.geometry;
//                     const x = xMin * canvas.width;
//                     const y = yMin * canvas.height;
//                     const width = (xMax - xMin) * canvas.width;
//                     const height = (yMax - yMin) * canvas.height;
//                     ctx.strokeRect(x, y, width, height);
//                 }
//             );
//         }
//     );
// }

// function findWordInBox(ocrData: any, x: number, y: number) {
//     for (const blockWords of ocrData!) {
//         const words = blockWords.words;
//         for (const word of words) {
//             const [[xMin, yMin], [xMax, yMax]] = word.geometry;
//             const isInBox = x >= xMin && x <= xMax && y >= yMin && y <= yMax;
//             console.log(isInBox);
//             if (isInBox) {
//                 return { word: word.value, geometry: word.geometry };            
//             }
//         }
//     }
//     return null;
// }

// export default function Canvas() {
//     const canvasRef = useRef<HTMLCanvasElement>(null);
//     const [ocrData, setOcrData] = useState<any>();
//     const [foundedWord, setFoundedWord] = useState<{ word: string, geometry: [[number, number], [number, number]] } | null>(null);

//     const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
//         const files = event.target.files;
//         const newFormData = new FormData();
//         newFormData.append("file", files?.[0] as File);
//         const {
//             images,
//             result
//         }: UploadPdfResponse = await uploadPdf(newFormData) as UploadPdfResponse;
        
//         const blob = base64ToBlob(images[0], "image/jpeg");
        
//         const imgURL = URL.createObjectURL(blob);
//         const img = new Image();
//         img.src = imgURL;
//         await img.decode();
//         const canvas = canvasRef.current!;
//         const ctx = canvas?.getContext('2d');
//         canvas.width = img.width;
//         canvas.height = img.height;
//         ctx?.drawImage(img, 0, 0, img.width, img.height);
//         const boxes = result?.pages[0]?.blocks[0]?.lines;
//         setOcrData(boxes!);
//         console.log(boxes);
//         drawBoxes(ctx!, boxes!, canvas);
//     }

//     const handleCanvasClick = (event: React.MouseEvent<HTMLCanvasElement>) => {
//         const canvas = canvasRef.current!;
//         const ctx = canvas?.getContext('2d');
//         const rect = canvas.getBoundingClientRect();
//         const x = ((event.clientX - rect.left) / rect.width);
//         const y = ((event.clientY - rect.top) / rect.height);
//         const currentWord = findWordInBox(ocrData!, x, y);
//         setFoundedWord(currentWord);
//     }

//     return (
//         <>
//             <input type="file" accept="application/pdf" multiple onChange={handleFileChange} />
//             <p>The word founded is: {foundedWord?.word} / {foundedWord?.geometry}</p>
//             <aside className="flex flex-row gap-4 w-2/3 h-[1000px] bg-red-500">
//                 <canvas id="canvas"
//                     ref={canvasRef}
//                     onClick={handleCanvasClick}
//                     className="bg-blue-500"
//                 />
//             </aside>
//         </>
//     );
// }