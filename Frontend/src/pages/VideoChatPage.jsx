import React from 'react';
import VideoPlayer from '../components/VideoPlayer';
import ChatBox from '../components/ChatBox';
import GradientButton from '../components/GradientButton';

/** Video and Chat Interface Page */
const VideoChatPage = ({ videoUrl, handleLogout, handleNext }) => {
    return (
        <div className="flex flex-col p-4 md:p-8 overflow-hidden">
            <div className="flex justify-between mb-4">
                <GradientButton onClick={handleLogout} className="px-6">
                    Go Back to Dashboard
                </GradientButton>
                <GradientButton onClick={handleNext} className="px-6">
                    Next
                </GradientButton>
            </div>

            <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
                {/* Left Section */}
                <div className="lg:col-span-2 flex flex-col overflow-hidden">
                    <div className="flex-1 overflow-hidden">
                        <VideoPlayer videoUrl={videoUrl} />
                    </div>
                </div>

                {/* Right Section: Chatbox scrolls internally */}
                <ChatBox videoUrl={videoUrl} />
            </div>
        </div>
    );
};

export default VideoChatPage;
