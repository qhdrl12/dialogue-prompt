import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Link from 'next/link';
import { FaLightbulb, FaMagic, FaRocket, FaUserAlt, FaCode, FaChartLine } from 'react-icons/fa';

export default function About() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      
      <div className="flex-grow">
        {/* 소개 */}
        <section className="py-16 md:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-4xl mx-auto text-center">
              <h1 className="text-4xl md:text-5xl font-serif font-bold text-secondary-900 mb-8">
                프롬프트 생성기 <span className="bg-clip-text text-transparent bg-gradient-to-r from-primary-500 to-accent-500">소개</span>
              </h1>
              
              <p className="text-xl text-secondary-600 mb-8 leading-relaxed">
                프롬프트 생성기는 사용자의 간단한 키워드 또는 설명을 바탕으로, 
                목표 달성에 최적화된 구체적인 프롬프트를 생성하는 AI 기반 서비스입니다.
              </p>
              
              <div className="holy-card">
                <p className="text-secondary-700 mb-4">
                  AI 언어 모델의 기술 발전으로 다양한 작업이 가능해졌지만, 여전히 좋은 결과를 얻기 위해서는 
                  명확하고 구체적인 프롬프트가 필요합니다. 저희 서비스는 이 과정을 간소화하고, 누구나 쉽게 
                  최적화된 프롬프트를 만들 수 있도록 도와드립니다.
                </p>
                <p className="text-secondary-700">
                  Langchain과 Langgraph를 기반으로 개발된 AI 엔진이 사용자의 목표를 파악하고, 
                  최적의 프롬프트를 생성하여 즉시 OpenAI 및 Gemini API를 통해 결과를 확인할 수 있습니다.
                </p>
              </div>
            </div>
          </div>
        </section>
        
        {/* 주요 기능 */}
        <section className="py-16 bg-white bg-opacity-70">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-serif font-bold text-center text-secondary-900 mb-12">
              주요 기능
            </h2>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div className="holy-card flex items-start">
                <div className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-primary-100 text-primary-600 mr-4">
                  <FaMagic className="text-xl" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">AI 프롬프트 생성</h3>
                  <p className="text-secondary-600">
                    키워드나 간단한 설명만으로 다양한 관점의 최적화된 프롬프트를 자동으로 생성합니다.
                    명확성을 높이기 위한 추가 질문을 통해 더 구체적인 프롬프트를 만들 수 있습니다.
                  </p>
                </div>
              </div>
              
              <div className="holy-card flex items-start">
                <div className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-accent-100 text-accent-600 mr-4">
                  <FaRocket className="text-xl" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">LLM 즉시 테스트</h3>
                  <p className="text-secondary-600">
                    생성된 프롬프트를 OpenAI API 또는 Gemini API를 통해 즉시 실행하고 결과를 확인할 수 있습니다.
                    모델 선택과 주요 파라미터 설정을 통해 결과를 세밀하게 조정할 수 있습니다.
                  </p>
                </div>
              </div>
              
              <div className="holy-card flex items-start">
                <div className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-primary-100 text-primary-600 mr-4">
                  <FaLightbulb className="text-xl" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">다양한 프롬프트 제안</h3>
                  <p className="text-secondary-600">
                    다양한 버전의 구체적인 프롬프트를 생성하여 제시합니다.
                    각 프롬프트에는 목적, 예상 결과, 특징 등을 설명하여 선택을 돕습니다.
                  </p>
                </div>
              </div>
              
              <div className="holy-card flex items-start">
                <div className="flex-shrink-0 w-12 h-12 flex items-center justify-center rounded-full bg-accent-100 text-accent-600 mr-4">
                  <FaChartLine className="text-xl" />
                </div>
                <div>
                  <h3 className="text-xl font-bold mb-2">프롬프트 저장 및 관리</h3>
                  <p className="text-secondary-600">
                    마음에 드는 프롬프트와 그 결과를 저장하고 추후에 다시 불러올 수 있습니다.
                    히스토리 기능을 통해 이전에 생성하고 테스트했던 프롬프트들을 확인할 수 있습니다.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
        
        {/* 목표 사용자 */}
        <section className="py-16">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-serif font-bold text-center text-secondary-900 mb-12">
              이런 분들께 추천합니다
            </h2>
            
            <div className="grid md:grid-cols-3 gap-8">
              <div className="holy-card text-center">
                <div className="w-16 h-16 mx-auto flex items-center justify-center rounded-full bg-primary-100 text-primary-600 mb-4">
                  <FaUserAlt className="text-xl" />
                </div>
                <h3 className="text-xl font-bold mb-2">콘텐츠 크리에이터</h3>
                <p className="text-secondary-600">
                  블로그 게시물, 소셜 미디어 콘텐츠, 마케팅 문구 등 다양한 콘텐츠 아이디어를 구체화하고 
                  결과물의 품질을 높이고자 하는 분들
                </p>
              </div>
              
              <div className="holy-card text-center">
                <div className="w-16 h-16 mx-auto flex items-center justify-center rounded-full bg-accent-100 text-accent-600 mb-4">
                  <FaCode className="text-xl" />
                </div>
                <h3 className="text-xl font-bold mb-2">개발자 및 기획자</h3>
                <p className="text-secondary-600">
                  특정 기능이나 아이디어를 LLM을 통해 프로토타이핑하거나 구체적인 결과물을 얻고자 하는 분들
                </p>
              </div>
              
              <div className="holy-card text-center">
                <div className="w-16 h-16 mx-auto flex items-center justify-center rounded-full bg-primary-100 text-primary-600 mb-4">
                  <FaChartLine className="text-xl" />
                </div>
                <h3 className="text-xl font-bold mb-2">마케터 및 연구원</h3>
                <p className="text-secondary-600">
                  시장 조사, 데이터 분석, 보고서 작성 등 특정 목적에 맞는 정보를 LLM으로부터 
                  효율적으로 얻고자 하는 분들
                </p>
              </div>
            </div>
          </div>
        </section>
        
        {/* CTA */}
        <section className="py-16 mb-8">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="max-w-3xl mx-auto holy-card text-center">
              <h2 className="text-3xl font-serif font-bold text-secondary-900 mb-6">
                지금 바로 시작하세요
              </h2>
              
              <p className="text-lg text-secondary-600 mb-8">
                언어 모델의 잠재력을 최대한 활용할 수 있는 최적의 프롬프트를 생성하고, 
                이를 통해 더 나은 결과를 얻어보세요.
              </p>
              
              <Link 
                href="/create" 
                className="holy-button text-lg px-8 py-3 inline-block"
              >
                프롬프트 생성하기
              </Link>
            </div>
          </div>
        </section>
      </div>
      
      <Footer />
    </main>
  );
}