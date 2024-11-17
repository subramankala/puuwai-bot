// src/ChatbotComponent.js
import React, { useState } from 'react';
import axios from 'axios';

const ChatbotComponent = () => {
  const [showChat, setShowChat] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const toggleChat = () => {
    setShowChat((prev) => !prev);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput('');

    try {
      const response = await axios.post(
        'https://api.openai.com/v1/chat/completions',
        {
          model: 'gpt-3.5-turbo',
          messages: updatedMessages,
        },
        {
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
          },
        }
      );

      const botMessage = {
        role: 'assistant',
        content: response.data.choices[0].message.content.trim(),
      };
      setMessages([...updatedMessages, botMessage]);
    } catch (error) {
      console.error('Error fetching response:', error);
    }
  };

  return (
    <div>
      <button style={styles.chatButton} onClick={toggleChat}>
        <img src="chat-icon.png" alt="Chat" style={styles.chatIcon} />
      </button>

      {showChat && (
        <div style={styles.chatWindow}>
          <div style={styles.header}>
            <h4 style={styles.headerText}>TayoBot</h4>
            <button style={styles.closeButton} onClick={toggleChat}>×</button>
          </div>
          <div style={styles.messagesContainer}>
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  ...styles.message,
                  alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  backgroundColor: msg.role === 'user' ? '#0078d4' : '#f0f0f0',
                  color: msg.role === 'user' ? '#fff' : '#000',
                }}
              >
                {msg.content}
              </div>
            ))}
          </div>
          <div style={styles.inputContainer}>
            <input
              style={styles.input}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
            />
            <button style={styles.sendButton} onClick={handleSend}>
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  chatButton: {
    position: 'fixed',
    bottom: '20px',
    right: '20px',
    backgroundColor: '#0078d4',
    borderRadius: '50%',
    width: '60px',
    height: '60px',
    border: 'none',
    cursor: 'pointer',
    zIndex: 1000,
  },
  chatIcon: {
    width: '30px',
    height: '30px',
  },
  chatWindow: {
    position: 'fixed',
    bottom: '80px',
    right: '20px',
    width: '350px',
    height: '500px',
    border: '1px solid #ccc',
    borderRadius: '10px',
    backgroundColor: '#fff',
    zIndex: 1000,
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0 2px 10px rgba(0,0,0,0.2)',
  },
  header: {
    padding: '10px',
    backgroundColor: '#0078d4',
    color: '#fff',
    borderTopLeftRadius: '10px',
    borderTopRightRadius: '10px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerText: {
    margin: 0,
  },
  closeButton: {
    background: 'none',
    border: 'none',
    color: '#fff',
    fontSize: '20px',
    cursor: 'pointer',
  },
  messagesContainer: {
    flex: 1,
    padding: '10px',
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
  },
  message: {
    maxWidth: '80%',
    padding: '10px',
    borderRadius: '10px',
    marginBottom: '10px',
  },
  inputContainer: {
    display: 'flex',
    borderTop: '1px solid #ccc',
  },
  input: {
    flex: 1,
    padding: '10px',
    border: 'none',
    outline: 'none',
  },
  sendButton: {
    padding: '10px 20px',
    border: 'none',
    backgroundColor: '#0078d4',
    color: '#fff',
    cursor: 'pointer',
  },
};

export default ChatbotComponent;
