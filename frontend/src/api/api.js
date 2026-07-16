import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
});

export const getDocuments = async () => {
  const response = await api.get("/documents");
  return response.data;
};

export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/documents/upload",
    formData
  );

  return response.data;
};

export const chatWithDocument = async ({
  query,
  documentId,
  sessionId = "default",
  topK = 3,
}) => {
  const response = await api.post("/chat", {
    query: query,
    document_id: documentId,
    top_k: topK,
    session_id: sessionId,
  });

  return response.data;
};

export const deleteDocument = async (documentId) => {
  const response = await api.delete(
    `/documents/${documentId}`
  );

  return response.data;
};

export default api;