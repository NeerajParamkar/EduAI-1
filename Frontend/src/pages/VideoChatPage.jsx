import React from 'react';
import VideoPlayer from '../components/VideoPlayer';
import ChatBox from '../components/ChatBox';
import GradientButton from '../components/GradientButton';

/** Video and Chat Interface Page */
const VideoChatPage = ({ videoUrl, handleLogout }) => {
    return (
        <div className="flex-1 flex flex-col p-4 md:p-8">
            <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Section: Video Player (approx 70% on desktop) */}
                <div className="lg:col-span-2 flex flex-col">
                    <VideoPlayer videoUrl={videoUrl} />
                    <div className='lg:hidden'>
                        <GradientButton onClick={handleLogout} className="w-full mt-4">
                            Go Back to Dashboard
                        </GradientButton>
                    </div>
                </div>

                {/* Right Section: AI Chatbot Panel (approx 30% on desktop) */}
                <ChatBox videoUrl={videoUrl} />
            </div>

            <div className='hidden lg:block'>
                <GradientButton onClick={handleLogout} className="max-w-xs mx-auto mt-6">
                    Go Back to Dashboard
                </GradientButton>
            </div>
        </div>
    );
};

export default VideoChatPage;