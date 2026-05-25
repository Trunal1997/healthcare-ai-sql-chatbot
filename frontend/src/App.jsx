import { useState } from 'react';
import axios from 'axios';
import { Bot, User, Send, Database, ShieldCheck, Activity, Stethoscope } from 'lucide-react';

const API_URL = 'http://127.0.0.1:8000/chat';

const sampleQuestions = [
  'Show diabetic patients above age 50 from Pune',
  'Show unpaid bills above 5000',
  'Show today appointments',
  'Show all patients from Nagpur'
];

function ResultTable({ data }) {
  if (!data || data.length === 0) return null;
  const columns = Object.keys(data[0]);

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => <td key={column}>{String(row[column] ?? '')}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role === 'user';

  return (
    <div className={`message-row ${isUser ? 'right' : 'left'}`}>
      <div className={`avatar ${isUser ? 'user-avatar' : 'bot-avatar'}`}>
        {isUser ? <User size={18} /> : <Bot size={18} />}
      </div>

      <div className={`bubble ${isUser ? 'user-bubble' : 'bot-bubble'}`}>
        <p>{message.text}</p>

        {message.sql && (
          <div className="sql-box">
            <div className="sql-title"><Database size={15} /> Generated SQL</div>
            <pre>{message.sql}</pre>
          </div>
        )}

        {message.data && message.data.length > 0 && (
          <div className="result-box">
            <div className="sql-title"><Activity size={15} /> Result</div>
            <ResultTable data={message.data} />
          </div>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Hello! I am your Healthcare AI SQL Assistant. Ask me about patients, appointments, diagnosis, or billing records.'
    }
  ]);

  const sendMessage = async (customQuestion) => {
    const question = (customQuestion || input).trim();
    if (!question || loading) return;

    const userMessage = { role: 'user', text: question };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(API_URL, { message: question });
      const botMessage = {
        role: 'assistant',
        text: response.data.assistant_message,
        sql: response.data.sql_query,
        data: response.data.data
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: error.response?.data?.detail || 'Something went wrong. Please check backend and database connection.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Stethoscope size={25} /></div>
          <div>
            <h1>Healthcare AI</h1>
            <p>Text-to-SQL Chatbot</p>
          </div>
        </div>

        <div className="info-card">
          <ShieldCheck size={22} />
          <div>
            <strong>Safe SQL Execution</strong>
            <span>Only SELECT queries are allowed.</span>
          </div>
        </div>

        <div className="examples">
          <h3>Try these questions</h3>
          {sampleQuestions.map((question) => (
            <button key={question} onClick={() => sendMessage(question)} disabled={loading}>
              {question}
            </button>
          ))}
        </div>
      </aside>

      <main className="chat-panel">
        <header className="chat-header">
          <div>
            <h2>Healthcare SQL Assistant</h2>
            <p>Ask in plain English. The AI generates SQL and returns results.</p>
          </div>
          <span className="status-dot">● Online</span>
        </header>

        <section className="messages">
          {messages.map((message, index) => <MessageBubble key={index} message={message} />)}
          {loading && (
            <div className="message-row left">
              <div className="avatar bot-avatar"><Bot size={18} /></div>
              <div className="bubble bot-bubble typing">Generating SQL and fetching data...</div>
            </div>
          )}
        </section>

        <footer className="composer">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask: Show diabetic patients above age 50 from Pune"
          />
          <button onClick={() => sendMessage()} disabled={loading || !input.trim()}>
            <Send size={18} /> Send
          </button>
        </footer>
      </main>
    </div>
  );
}
