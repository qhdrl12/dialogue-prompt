'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { FaArrowRight, FaSpinner, FaStar, FaCopy, FaInfoCircle } from 'react-icons/fa';
import axios from 'axios';

interface Prompt {
  prompt: string;
  description: string;
}

interface AdditionalQuestion {
  id: string;
  question: string;
  answer: string;
  options?: string[];
}

export default function Home() {
  const [keywords, setKeywords] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<string | null>(null);
  const [additionalQuestions, setAdditionalQuestions] = useState<AdditionalQuestion[]>([]);
  const [showAdditionalQuestions, setShowAdditionalQuestions] = useState(false);
  const [selectedModel, setSelectedModel] = useState('gpt-4.1');
  const [isSubmitDisabled, setIsSubmitDisabled] = useState(false);
  const [requirementFeedback, setRequirementFeedback] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!keywords.trim()) return;
    
    setIsLoading(true);
    setPrompts([]);
    setSelectedPrompt(null);
    
    try {
      const response = await axios.post('http://localhost:8000/prompt/generate', {
        keywords: keywords.trim(),
        additionalInfo: additionalQuestions.reduce((acc, q) => {
          acc[q.id] = q.answer;
          return acc;
        }, {} as Record<string, string>)
      });
      
      setPrompts(response.data.prompts);
      
      if (response.data.needMoreInfo) {
        setAdditionalQuestions([
          {
            id: 'target',
            question: '대상 독자/고객은 누구인가요?',
            answer: '',
            options: ['일반 사용자', '전문가/개발자', '학생', '비즈니스 리더']
          },
          {
            id: 'tone',
            question: '어떤 톤과 스타일로 작성할까요?',
            answer: '',
            options: ['전문적/학술적', '친근한/대화체', '간결한/명확한', '창의적/영감을 주는']
          },
          {
            id: 'goal',
            question: '주요 목표는 무엇인가요?',
            answer: '',
            options: ['정보 제공', '설득/제안', '문제 해결', '아이디어 브레인스토밍']
          }
        ]);
        setShowAdditionalQuestions(true);
      }
    } catch (error) {
      console.error('Error generating prompts:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePromptSelect = (prompt: string) => {
    setSelectedPrompt(prompt);
  };
  
  const handleCopyPrompt = (text: string) => {
    navigator.clipboard.writeText(text);
  };
  
  const handleAdditionalQuestionChange = (id: string, value: string) => {
    setAdditionalQuestions(
      additionalQuestions.map(q => q.id === id ? { ...q, answer: value } : q)
    );
  };
  
  const handleApplyAdditionalInfo = async () => {
    if (isSubmitDisabled || isLoading) return;
    
    // Disable button to prevent multiple rapid clicks
    setIsSubmitDisabled(true);
    setIsLoading(true);
    setRequirementFeedback(null);
    
    try {
      const response = await axios.post('http://localhost:8000/prompt/generate', {
        keywords: keywords.trim(),
        model: selectedModel,
        additionalInfo: additionalQuestions.reduce((acc, q) => {
          acc[q.id] = q.answer;
          return acc;
        }, {} as Record<string, string>)
      });
      
      console.log("Server response:", response.data);
      
      // Force a minimum processing time to prevent flickering
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (response.data.needMoreInfo) {
        // Still need more info, update questions and keep asking
        setRequirementFeedback(response.data.feedback || '추가 정보가 필요합니다.');
        if (response.data.questions && response.data.questions.length > 0) {
          setAdditionalQuestions(response.data.questions);
        }
        setShowAdditionalQuestions(true);
      } else if (response.data.prompts && response.data.prompts.length > 0) {
        // Got prompts, show them
        console.log("Setting prompts:", response.data.prompts);
        setPrompts(response.data.prompts);
        setShowAdditionalQuestions(false);
        // 프롬프트 생성이 완료되면 additionalQuestions 초기화
        setAdditionalQuestions([]);
      } else {
        // Handle case where no prompts were returned
        console.error("No prompts in response:", response.data);
        setRequirementFeedback('프롬프트를 생성할 수 없습니다. 다른 키워드를 시도해보세요.');
        setShowAdditionalQuestions(false);
      }
    } catch (error) {
      console.error('Error generating prompts:', error);
      if (axios.isAxiosError(error)) {
        console.error('Axios error details:', {
          status: error.response?.status,
          data: error.response?.data,
          message: error.message
        });
      }
      setRequirementFeedback('서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
      setShowAdditionalQuestions(false);
    } finally {
      setIsLoading(false);
      // Re-enable button after a short delay to prevent rapid clicking
      setTimeout(() => {
        setIsSubmitDisabled(false);
      }, 300);
    }
  };

  return (
    <main className="min-h-screen flex flex-col bg-gradient-to-br from-[#0a192f] via-[#112240] to-[#1a3a6e] text-[#e6f1ff]">
      <Header />
      
      <div className="flex-grow py-8 md:py-12 relative">
        <div className="absolute inset-0 bg-[url('/city-skyline-blur.jpg')] bg-cover bg-center opacity-20 pointer-events-none"></div>
        <div className="absolute inset-0 bg-black/30 pointer-events-none"></div>

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-12 md:mb-16">
              <h1 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-[#64ffda] to-[#00c6ff] mb-4 tracking-tight">
                Prompt Generator
              </h1>
            </div>
            
            <div className="mb-10 md:mb-12 bg-[#0f2d54]/50 backdrop-blur-md border border-[#2c4b78] shadow-2xl rounded-lg p-6 md:p-8">
              <div className="mb-6">
                <label htmlFor="keywordsInput" className="block mb-2 text-lg text-[#a8b2d1]">Your Topic or Keywords</label>
                <textarea
                  id="keywordsInput"
                  className="w-full p-4 bg-[#0a192f]/70 text-[#e6f1ff] border border-[#2c4b78] rounded-md
                  focus:ring-2 focus:ring-[#64ffda] focus:border-[#64ffda] transition-all duration-300
                  text-base md:text-lg placeholder:text-[#7f8cbe] min-h-[100px]"
                  placeholder="e.g., Future of AI in healthcare, Sci-fi story concept, Marketing copy for a new tech product..."
                  value={keywords}
                  onChange={(e) => setKeywords(e.target.value)}
                  rows={3}
                />
              </div>
              
              <div>
                <label htmlFor="modelSelect" className="block mb-2 text-lg text-[#a8b2d1]">Select AI Model</label>
                <select 
                  id="modelSelect"
                  className="w-full p-3 bg-[#0a192f]/70 text-[#e6f1ff] border border-[#2c4b78] rounded-md
                  focus:ring-2 focus:ring-[#64ffda] focus:border-[#64ffda] transition-all duration-300
                  text-base md:text-lg appearance-none custom-select"
                  value={selectedModel}
                  onChange={(e) => setSelectedModel(e.target.value)}
                >
                  <optgroup label="OpenAI Models" className="bg-[#0a192f]">
                    <option value="gpt-4.1">GPT-4.1 (Advanced Multimodal)</option>
                    <option value="gpt-4.1-nano">GPT-4.1 Nano (Lightweight)</option>
                    <option value="o4-mini">O4-Mini (Fast & Efficient)</option>
                  </optgroup>
                  <optgroup label="Gemini Models" className="bg-[#0a192f]">
                    <option value="gemini-2.5-flash-preview-04-17">
                      Gemini 2.5 Flash (Preview 04-17)
                    </option>
                  </optgroup>
                </select>
              </div>
            </div>
            
            <div className="flex justify-center mb-12 md:mb-16">
              <button 
                onClick={handleSubmit}
                className="px-8 py-3 bg-gradient-to-r from-[#64ffda] to-[#00c6ff] hover:opacity-90 text-[#0a192f] font-semibold text-lg
                rounded-md shadow-lg transition-all duration-300 transform hover:scale-105 flex items-center justify-center tracking-wide"
                disabled={isLoading || !keywords.trim()}
              >
                {isLoading ? (
                  <>
                    <FaSpinner className="animate-spin mr-2" />
                    Generating...
                  </>
                ) : (
                  <>
                    Generate Prompt
                    <FaArrowRight className="ml-2" />
                  </>
                )}
              </button>
            </div>
            
            {showAdditionalQuestions && (
              <div className="mb-10 md:mb-12 bg-[#0f2d54]/50 backdrop-blur-md border border-[#2c4b78] shadow-2xl rounded-lg p-6 md:p-8">
                <div className="flex items-center mb-6">
                  <FaInfoCircle className="text-[#64ffda] mr-3 text-xl" />
                  <h2 className="text-xl md:text-2xl font-semibold text-[#e6f1ff]">Refine Your Prompt</h2>
                </div>
                <div className="space-y-6">
                  {additionalQuestions.map((q) => (
                    <div key={q.id}>
                      <label className="block mb-2 text-base md:text-lg text-[#a8b2d1]">{q.question}</label>
                      {q.options ? (
                        <div className="flex flex-wrap gap-3">
                          {q.options.map((option) => (
                            <button
                              key={option}
                              type="button"
                              className={`px-4 py-2 text-sm md:text-base rounded-md transition-all duration-300 font-medium ${
                                q.answer === option
                                  ? 'bg-[#64ffda] text-[#0a192f] border border-[#64ffda]'
                                  : 'bg-[#0a192f]/70 text-[#a8b2d1] border border-[#2c4b78] hover:border-[#64ffda] hover:text-[#64ffda]'
                              }`}
                              onClick={() => handleAdditionalQuestionChange(q.id, option)}
                            >
                              {option}
                            </button>
                          ))}
                        </div>
                      ) : (
                        <input
                          type="text"
                          className="w-full p-3 bg-[#0a192f]/70 text-[#e6f1ff] border border-[#2c4b78] rounded-md
                          focus:ring-2 focus:ring-[#64ffda] focus:border-[#64ffda] transition-all duration-300
                          text-base md:text-lg placeholder:text-[#7f8cbe]"
                          value={q.answer}
                          onChange={(e) => handleAdditionalQuestionChange(q.id, e.target.value)}
                          placeholder="Your answer here..."
                        />
                      )}
                    </div>
                  ))}
                </div>
                <button
                  className="mt-8 px-6 py-2 bg-gradient-to-r from-[#64ffda] to-[#00c6ff] hover:opacity-90 text-[#0a192f] font-semibold 
                  rounded-md shadow-md transition-all duration-300 transform hover:scale-105 tracking-wide"
                  onClick={handleApplyAdditionalInfo}
                  disabled={additionalQuestions.some(q => !q.answer)}
                >
                  Apply & Regenerate
                </button>
              </div>
            )}
            
            {prompts.length > 0 && (
              <div>
                <h2 className="text-2xl md:text-3xl font-semibold text-center text-[#e6f1ff] mb-8 flex items-center justify-center">
                  <FaStar className="text-[#ffc107] mr-3" /> 
                  Generated Prompts
                </h2>
                
                <div className="grid md:grid-cols-2 gap-6 md:gap-8">
                  {prompts.map((promptItem, index) => (
                    <div 
                      key={index}
                      className={`bg-[#0f2d54]/50 backdrop-blur-md border transition-all duration-300 rounded-lg p-6 shadow-lg hover:shadow-2xl hover:border-[#64ffda] cursor-pointer ${
                        selectedPrompt === promptItem.prompt 
                          ? 'border-[#64ffda] shadow-2xl ring-2 ring-[#64ffda]/50' 
                          : 'border-[#2c4b78]'
                      }`}
                      onClick={() => handlePromptSelect(promptItem.prompt)}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <h3 className="text-lg md:text-xl font-semibold text-[#64ffda]">
                          {promptItem.description}
                        </h3>
                        <button 
                          className="text-[#a8b2d1] hover:text-[#64ffda] p-1 transition-colors"
                          onClick={(e) => {
                            e.stopPropagation();
                            handleCopyPrompt(promptItem.prompt);
                          }}
                          title="Copy Prompt"
                        >
                          <FaCopy />
                        </button>
                      </div>
                      <p className="text-[#cdd6f7] text-sm md:text-base bg-[#0a192f]/50 p-3 rounded-md border border-[#1f3a61]">
                        {promptItem.prompt}
                      </p>
                    </div>
                  ))}
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
