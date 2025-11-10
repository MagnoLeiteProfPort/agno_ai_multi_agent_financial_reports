import React from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * Report component — renders markdown into styled HTML.
 */
export default function Report({ content }) {
  return (
    <div className="prose prose-lg max-w-none text-gray-800">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {content}
      </ReactMarkdown>
    </div>
  );
}
