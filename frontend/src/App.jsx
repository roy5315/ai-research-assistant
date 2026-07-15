import { useEffect, useState } from "react";
import {
  getDocuments,
  uploadDocument,
  chatWithDocument,
  deleteDocument,
} from "./api/api";

import "./App.css";

function App() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocument, setSelectedDocument] = useState(null);
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const loadDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data.documents);
    } catch (error) {
      console.error("Failed to load documents:", error);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const handleUpload = async () => {
    if (!file) return;

    try {
      setUploading(true);

      await uploadDocument(file);

      setFile(null);
      await loadDocuments();
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setUploading(false);
    }
  };

  const handleAsk = async () => {
    if (!query.trim() || !selectedDocument) return;

    const currentQuery = query;

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: currentQuery,
      },
    ]);

    setQuery("");
    setAsking(true);

    try {
      const data = await chatWithDocument({
        query: currentQuery,
        documentId: selectedDocument.document_id,
        sessionId: `document-${selectedDocument.document_id}`,
      });

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
        },
      ]);
    } catch (error) {
      console.error("Chat failed:", error);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          role: "assistant",
          content: "Unable to answer the question.",
        },
      ]);
    } finally {
      setAsking(false);
    }
  };

  const handleDelete = async (documentId) => {
    try {
      await deleteDocument(documentId);

      if (selectedDocument?.document_id === documentId) {
        setSelectedDocument(null);
        setMessages([]);
      }

      await loadDocuments();
    } catch (error) {
      console.error("Delete failed:", error);
    }
  };

  const selectDocument = (document) => {
    setSelectedDocument(document);
    setMessages([]);
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <h1>Research AI</h1>
          <p>Document Intelligence</p>
        </div>

        <div className="upload-section">
          <input
            type="file"
            accept=".pdf"
            onChange={(event) => setFile(event.target.files[0])}
          />

          <button
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? "Processing..." : "Upload PDF"}
          </button>
        </div>

        <div className="documents">
          <h2>Documents</h2>

          {documents.length === 0 && (
            <p className="empty-text">No documents uploaded.</p>
          )}

          {documents.map((document) => (
            <div
              key={document.document_id}
              className={`document-item ${
                selectedDocument?.document_id === document.document_id
                  ? "active"
                  : ""
              }`}
            >
              <button
                className="document-select"
                onClick={() => selectDocument(document)}
              >
                <span>PDF</span>
                <p>{document.filename}</p>
              </button>

              <button
                className="delete-button"
                onClick={() => handleDelete(document.document_id)}
              >
                ×
              </button>
            </div>
          ))}
        </div>
      </aside>

      <main className="chat-container">
        {!selectedDocument ? (
          <div className="welcome">
            <h2>AI Research Assistant</h2>

            <p>
              Upload and select a research document to begin exploring it.
            </p>
          </div>
        ) : (
          <>
            <header className="chat-header">
              <div>
                <p>Research document</p>
                <h2>{selectedDocument.filename}</h2>
              </div>
            </header>

            <section className="messages">
              {messages.length === 0 && (
                <div className="empty-chat">
                  <h3>Ask your document anything</h3>

                  <p>
                    Explore concepts, methods, results, and technical details.
                  </p>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`message ${message.role}`}
                >
                  <div className="message-role">
                    {message.role === "user" ? "You" : "Research AI"}
                  </div>

                  <div className="message-content">
                    {message.content}
                  </div>

                  {message.sources?.length > 0 && (
                    <div className="sources">
                      <p>Sources</p>

                      {message.sources.map((source, sourceIndex) => (
                        <span key={sourceIndex}>
                          Chunk {source.chunk_index} ·{" "}
                          {Number(source.score).toFixed(3)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {asking && (
                <div className="message assistant">
                  <div className="message-role">Research AI</div>

                  <div className="message-content">
                    Thinking...
                  </div>
                </div>
              )}
            </section>

            <div className="chat-input-container">
              <textarea
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    handleAsk();
                  }
                }}
                placeholder="Ask a question about this document..."
                rows="1"
              />

              <button
                onClick={handleAsk}
                disabled={!query.trim() || asking}
              >
                Ask
              </button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;