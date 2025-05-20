'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { FaArrowRight, FaSpinner } from 'react-icons/fa';
import axios from 'axios';

interface Prompt {
  prompt: string;
  description: string;
}

export default function CreatePrompt() {
  const [keywords, setKeywords] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const [llmResult, setLlmResult] = useState<string | null>(null);
  const [llmLoading, setLlmLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!keywords.trim()) return;
    
    setIsLoading(true);
    setPrompts([]);
    setSelectedPrompt(null);
    setLlmResult(null);
    
    try {
      // 백엔드 API 호출
      const response = await axios.post('http://localhost:8000/prompt/generate', {
        keywords: keywords.trim(),
      });
      
      setPrompts(response.data.prompts);
    } catch (error) {
      console.error('Error generating prompts:', error);
      // 실제 구현에서는 적절한 오류 처리 추가
    } finally {
      setIsLoading(false);
    }
  };

  const handlePromptSelect = (prompt: string) => {
    setSelectedPrompt(prompt);
  };

  const handleTestPrompt = async () => {
    if (!selectedPrompt) return;
    
    setLlmLoading(true);
    setLlmResult(null);
    
    try {
      // 백엔드 API 호출 (LLM 테스트)
      const response = await axios.post('http://localhost:8000/prompt/test', {
        prompt: selectedPrompt,
        model: 'gpt-3.5-turbo', // 기본 모델
      });
      
      setLlmResult(response.data.result);
    } catch (error) {
      console.error('Error testing prompt:', error);
      // 실제 구현에서는 적절한 오류 처리 추가
    } finally {
      setLlmLoading(false);
    }
  };

  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      
      <div className="flex-grow py-8 md:py-12">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-5xl mx-auto">
            <h1 className="text-3xl md:text-4xl font-serif font-bold text-secondary-900 mb-8 text-center">
              프롬프트 생성하기
            </h1>
            
            {/* 키워드 입력 폼 */}
            <form onSubmit={handleSubmit} className="mb-12">
              <div className="holy-card">
                <label htmlFor="keywords" className="block text-lg font-medium text-secondary-700 mb-2">
                  키워드 또는 간단한 설명을 입력하세요
                </label>
                <textarea
                  id="keywords"
                  className="holy-input min-h-[120px]"
                  placeholder="예: 디지털 마케팅 전략, 웹 개발 트렌드, AI 기반 콘텐츠 생성 등"
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                  required
                />
                <p className="text-sm text-secondary-500 mt-2">
                  당신의 목표를 간단하게 설명해주세요. 더 구체적인 내용은 추가 질문을 통해 수집됩니다.
                </p>
                
                <button 
                  type="submit" 
                  className="holy-button mt-4 flex items-center justify-center"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <FaSpinner className="animate-spin mr-2" />
                      프롬프트 생성 중...
                    </>
                  ) : (
                    <>
                      프롬프트 생성하기
                      <FaArrowRight className="ml-2" />
                    </>
                  )}
                </button>
              </div>
            </form>
            
            {/* 생성된 프롬프트 결과 */}
            {prompts.length > 0 && (
              <div className="mb-12">
                <h2 className="text-2xl font-serif font-bold text-secondary-900 mb-4">
                  생성된 프롬프트
                </h2>
                
                <div className="grid md:grid-cols-2 gap-6">
                  {prompts.map((promptItem, index) => (
                    <div 
                      key={index}
                      className={`holy-card cursor-pointer transition-all ${
                        selectedPrompt === promptItem.prompt 
                          ? 'border-primary-500 shadow-glow' 
                          : 'hover:border-primary-200'
                      }`}
                      onClick={() => handlePromptSelect(promptItem.prompt)}
                    >
                      <h3 className="text-lg font-medium text-secondary-800 mb-2">
                        {promptItem.description}
                      </h3>
                      <p className="text-secondary-600 text-sm border border-secondary-100 bg-secondary-50 p-3 rounded">
                        {promptItem.prompt}
                      </p>
                    </div>
                  ))}
                </div>
                
                {selectedPrompt && (
                  <div className="mt-6 flex justify-center">
                    <button 
                      className="holy-button"
                      onClick={handleTestPrompt}
                      disabled={llmLoading}
                    >
                      {llmLoading ? (
                        <>
                          <FaSpinner className="animate-spin mr-2" />
                          LLM 응답 생성 중...
                        </>
                      ) : 'LLM으로 테스트하기'}
                    </button>
                  </div>
                )}
              </div>
            )}
            
            {/* LLM 결과 */}
            {llmResult && (
              <div className="mb-12">
                <h2 className="text-2xl font-serif font-bold text-secondary-900 mb-4">
                  LLM 응답 결과
                </h2>
                
                <div className="holy-card">
                  <pre className="whitespace-pre-wrap text-secondary-700">
                    {llmResult}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      <Footer />
    </main>
  );
} 