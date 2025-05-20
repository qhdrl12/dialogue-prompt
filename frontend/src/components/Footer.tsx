import Link from 'next/link';
import { FaHeart, FaGithub } from 'react-icons/fa';

export default function Footer() {
  return (
    <footer className="w-full py-6 px-4 sm:px-6 lg:px-8 border-t border-secondary-100 backdrop-blur-sm bg-white bg-opacity-70">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-secondary-500 text-sm">
              © 2025 Dialogue Prompt. 모든 권리 보유.
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            <Link href="/terms" className="text-secondary-500 hover:text-primary-500 text-sm transition-colors">
              이용약관
            </Link>
            <Link href="/privacy" className="text-secondary-500 hover:text-primary-500 text-sm transition-colors">
              개인정보 처리방침
            </Link>
            <Link href="https://github.com" className="text-secondary-500 hover:text-primary-500 transition-colors">
              <FaGithub className="text-xl" />
            </Link>
          </div>
        </div>
        
        <div className="mt-4 text-center text-sm text-secondary-400">
          <p className="flex items-center justify-center">
            Made with <FaHeart className="text-accent-500 mx-1" /> using Next.js and Tailwind CSS
          </p>
        </div>
      </div>
    </footer>
  );
} 