"use client";

import { useEffect, useRef, useState } from "react";
import { pdfjs, Document, Page } from "react-pdf";
import "react-pdf/dist/Page/TextLayer.css";
import "react-pdf/dist/Page/AnnotationLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

export default function PDFViewer({ fileUrl, className = "" }) {
  const containerRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(0);
  const [numPages, setNumPages] = useState(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const el = containerRef.current;
    const ro = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (!entry) return;
      setContainerWidth(Math.floor(entry.contentRect.width));
    });

    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  return (
    <div ref={containerRef} className={className}>
      <div className="w-full flex flex-col items-center">
        <Document
          key={fileUrl}
          file={fileUrl}
          className="max-w-full"
          onLoadError={(error) => console.error(error)}
          loading={
            <div className="flex flex-col items-center justify-center w-full py-12 text-gray-400">
              <div className="w-8 h-8 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin mb-3" />
              <p className="text-sm">Loading Preview...</p>
            </div>
          }
          error={
            <div className="flex flex-col items-center justify-center w-full py-12 text-gray-400">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="w-10 h-10 mb-3"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1.5}
                  d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"
                />
              </svg>
              <p className="text-sm">Failed to load Preview</p>
            </div>
          }
          onLoadSuccess={({ numPages }) => {
            setNumPages(numPages);
          }}
        >
          {numPages &&
            Array.from({ length: numPages }, (_, i) => (
              <Page
                key={i + 1}
                pageNumber={i + 1}
                width={containerWidth || undefined}
              />
            ))}
        </Document>
      </div>
    </div>
  );
}
