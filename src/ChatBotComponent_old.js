// src/ChatBotComponent.js
import React, { useState } from 'react';
import axios from 'axios';

const ChatBotComponent = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

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
    <div style={styles.chatContainer}>
      <div style={styles.messagesContainer}>
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              ...styles.message,
              alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
              backgroundColor: msg.role === 'user' ? '#0078d4' : '#e5e5ea',
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
        <button style={styles.button} onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
};

const styles = {
  chatContainer: {
    display: 'flex',
    flexDirection: 'column',
    width: '400px',
    height: '500px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    overflow: 'hidden',
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
    borderRadius: '8px',
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
  button: {
    padding: '10px 20px',
    border: 'none',
    backgroundColor: '#0078d4',
    color: '#fff',
    cursor: 'pointer',
  },
};

export default ChatBotComponent;


