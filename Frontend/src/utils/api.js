const API_BASE_URL = 'http://localhost:8000/';

export const signup = async (email, password, confirmPassword) => {
    const response = await fetch(`${API_BASE_URL}auth/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            email, 
            password,
            confirm_password: confirmPassword  // ✅ Backend expects this field
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Signup failed');
    }

    return await response.json();
};

export const login = async (email, password) => {
    const response = await fetch(`${API_BASE_URL}auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
    }

    return await response.json();
};

export const processYoutubeUrl = async (url) => {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}transcript/process_url`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`, // Include auth token if needed
        },
        body: JSON.stringify({ url }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to process video URL');
    }

    return await response.json();
};


export const sendChatMessage = async (videoId, message, userEmail) => {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/send_message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ 
            video_id: videoId,
            message: message,
            user_email: userEmail
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to send message');
    }

    return await response.json();
};

/**
 * Get Chat History
 * Retrieves all previous chat messages for a specific video and user
 */
export const getChatHistory = async (videoId, userEmail) => {
    const token = localStorage.getItem('authToken');
    
    const response = await fetch(`${API_BASE_URL}/get_chat_history`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ 
            video_id: videoId,
            user_email: userEmail
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to get chat history');
    }

    return await response.json();
};