'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { FaTrash, FaCopy, FaRedo } from 'react-icons/fa';
import Link from 'next/link';

interface HistoryItem {
  id: string;
  date: string;
  keywords: string;
  selectedPrompt: string;
  result?: string;
}

export default function History() {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'favorites'>('all');
  
  useEffect(() => {
    // 로컬 스토리지에서 히스토리 아이템 로드
    // 실제 구현에서는 데이터베이스나 로컬 스토리지를 사용할 수 있습니다
    const dummyHistory: HistoryItem[] = [
      {
        id: '1',
        date: '2023-06-01T10:30:00',
        keywords: '디지털 마케팅 전략',
        selectedPrompt: '디지털 마케팅 분야의 전문가로서, 소셜 미디어를 활용한 마케팅 전략에 대해 자세히 설명해주세요.',
        result: '디지털 마케팅 전략에 대한 LLM 응답 결과입니다. 모델: gpt-3.5-turbo'
      },
      {
        id: '2',
        date: '2023-06-02T14:45:00',
        keywords: '웹 개발 트렌드',
        selectedPrompt: '2023년 웹 개발의 주요 트렌드와 이것이 개발자와 사용자 경험에 미치는 영향을 분석해주세요.',
        result: '웹 개발 트렌드에 대한 LLM 응답 결과입니다. 모델: gpt-3.5-turbo'
      },
      {
        id: '3',
        date: '2023-06-03T16:20:00',
        keywords: 'AI 기반 콘텐츠 생성',
        selectedPrompt: 'AI 기반 콘텐츠 생성 도구의 장단점을 분석하고, 콘텐츠 크리에이터가 이를 효과적으로 활용하는 방법을 제시해주세요.',
        result: 'AI 기반 콘텐츠 생성에 대한 LLM 응답 결과입니다. 모델: gpt-3.5-turbo'
      }
    ];
    
    setHistoryItems(dummyHistory);
  }, []);
  
  const handleDeleteItem = (id: string) => {
    setHistoryItems(prev => prev.filter(item => item.id !== id));
    // 실제 구현에서는 로컬 스토리지나 데이터베이스 업데이트
  };
  
  const handleCopyPrompt = (prompt: string) => {
    navigator.clipboard.writeText(prompt);
    // 복사 성공 알림을 표시할 수 있음
  };
  
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      
      <div className="flex-grow py-8 md:py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-5xl mx-auto">
            <h1 className="text-3xl md:text-4xl font-serif font-bold text-secondary-900 mb-8 text-center">
              프롬프트 히스토리
            </h1>
            
            {/* 탭 네비게이션 */}
            <div className="flex justify-center mb-8">
              <div className="inline-flex rounded-full border border-secondary-200 p-1">
                <button
                  className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                    activeTab === 'all'
                      ? 'bg-primary-500 text-white'
                      : 'text-secondary-700 hover:bg-secondary-50'
                  }`}
                  onClick={() => setActiveTab('all')}
                >
                  모든 기록
                </button>
                <button
                  className={`px-6 py-2 rounded-full text-sm font-medium transition-colors ${
                    activeTab === 'favorites'
                      ? 'bg-primary-500 text-white'
                      : 'text-secondary-700 hover:bg-secondary-50'
                  }`}
                  onClick={() => setActiveTab('favorites')}
                >
                  즐겨찾기
                </button>
              </div>
            </div>
            
            {/* 히스토리 목록 */}
            {historyItems.length > 0 ? (
              <div className="space-y-6">
                {historyItems.map(item => (
                  <div key={item.id} className="holy-card">
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="text-lg font-medium text-secondary-800">
                          {item.keywords}
                        </h3>
                        <p className="text-sm text-secondary-500">
                          {formatDate(item.date)}
                        </p>
                      </div>
                      <div className="flex space-x-2">
                        <button 
                          className="p-2 text-secondary-400 hover:text-primary-500 transition-colors"
                          onClick={() => handleCopyPrompt(item.selectedPrompt)}
                          title="프롬프트 복사"
                        >
                          <FaCopy />
                        </button>
                        <Link
                          href={`/create?prompt=${encodeURIComponent(item.selectedPrompt)}`}
                          className="p-2 text-secondary-400 hover:text-primary-500 transition-colors"
                          title="다시 사용하기"
                        >
                          <FaRedo />
                        </Link>
                        <button 
                          className="p-2 text-secondary-400 hover:text-accent-500 transition-colors"
                          onClick={() => handleDeleteItem(item.id)}
                          title="삭제"
                        >
                          <FaTrash />
                        </button>
                      </div>
                    </div>
                    
                    <div className="border border-secondary-100 bg-secondary-50 p-3 rounded mb-3">
                      <h4 className="text-sm font-medium text-secondary-700 mb-1">선택한 프롬프트:</h4>
                      <p className="text-secondary-600 text-sm">
                        {item.selectedPrompt}
                      </p>
                    </div>
                    
                    {item.result && (
                      <div>
                        <h4 className="text-sm font-medium text-secondary-700 mb-1">결과:</h4>
                        <p className="text-secondary-600 text-sm line-clamp-3">
                          {item.result}
                        </p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="holy-card text-center py-12">
                <p className="text-secondary-600 mb-4">
                  아직 저장된 히스토리가 없습니다.
                </p>
                <Link href="/create" className="holy-button inline-block">
                  프롬프트 생성하기
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
      
      <Footer />
    </main>
  );
} 