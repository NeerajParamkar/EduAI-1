import React from 'react';
import { Video } from 'lucide-react';
import { CARD_BG, PRIMARY_COLOR } from '../utils/constants';

/** Video Player Component with responsive 16:9 aspect ratio */
const VideoPlayer = ({ videoUrl }) => {
    const getEmbedId = (url) => {
        try {
            const urlObj = new URL(url);
            if (urlObj.hostname.includes('youtube.com')) {
                return urlObj.searchParams.get('v');
            } else if (urlObj.hostname.includes('youtu.be')) {
                return urlObj.pathname.substring(1);
            }
        } catch (e) {
            console.error("Invalid URL for embedding:", e);
        }
        // Fallback to a well-known educational video ID
        return 'LXb3fo5XOSo';
    };

    const embedId = getEmbedId(videoUrl) || 'LXb3fo5XOSo';
    const iframeSrc = `https://www.youtube.com/embed/${embedId}?autoplay=0&controls=1&modestbranding=1&rel=0`;

    return (
        <div className={`${CARD_BG} p-4 rounded-2xl shadow-xl border border-slate-700 mb-6 flex-1`}>
            <h2 className="text-xl font-bold text-white mb-3 flex items-center">
                <Video className={`w-6 h-6 mr-2 text-${PRIMARY_COLOR}-400`} /> Video Player
            </h2>
            {/* Responsive 16:9 Aspect Ratio Container */}
            <div className="relative w-full overflow-hidden rounded-xl" style={{ paddingTop: '56.25%' }}>
                <iframe
                    className="absolute top-0 left-0 w-full h-full"
                    src={iframeSrc}
                    frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    title="Embedded YouTube Video"> </iframe>
            </div>
        </div>
    );
};

export default VideoPlayer;