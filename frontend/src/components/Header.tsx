import Link from 'next/link';
import { FaLightbulb } from 'react-icons/fa';

export default function Header() {
  return (
    <header className="w-full py-5 bg-[#0a192f]/80 backdrop-blur-md border-b border-[#1f3a61] sticky top-0 z-50">
      <div className="container mx-auto">
        <Link href="/" className="flex items-center justify-center text-[#64ffda] transition-colors hover:text-[#52d8c8]">
          <FaLightbulb className="text-2xl md:text-3xl mr-3" />
          <span className="text-xl md:text-2xl font-semibold tracking-tight">
            
          </span>
        </Link>
      </div>
    </header>
  );
} 