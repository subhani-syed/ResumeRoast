import Link from "next/link";
export default function PrivacyPage() {
  return (
    <>
      <header className="fixed top-0 w-full z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between rounded border border-white/10 bg-white/5 backdrop-blur-xl shadow-lg px-6 py-3">
            <Link href="/" className="text-xl font-bold tracking-tight">
              Resume
              <span className="bg-linear-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
                Roast
              </span>
            </Link>
            <nav className="hidden md:flex items-center gap-8 text-sm text-gray-300">
              <Link href="/#features" className="hover:text-white transition">
                Features
              </Link>
              <Link href="/#reviews" className="hover:text-white transition">
                Reviews
              </Link>
              <Link href="/#faq" className="hover:text-white transition">
                FAQ
              </Link>
              <Link href="/privacy" className="hover:text-white transition">
                How It Works
              </Link>
              <Link
                href="/home"
                className="px-6 py-2 rounded bg-linear-to-r from-blue-500 to-cyan-500 text-sm font-semibold hover:opacity-90 transition"
              >
                Get Started
              </Link>
            </nav>
          </div>
        </div>
      </header>
      <main className="min-h-screen bg-white dark:bg-black text-gray-900 dark:text-gray-100">
        <div className="max-w-4xl mx-auto px-6 py-20">
          <div className="text-center mb-16">
            <h1 className="text-4xl font-bold tracking-tight mb-4">
              Privacy & Data Protection
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              How ResumeRoast protects your resume and personal information
            </p>
          </div>

          <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-12">
            ResumeRoast was built with privacy-first architecture. We understand
            that your resume contains sensitive personal information. Our system
            is designed to minimize data exposure, redact personally
            identifiable information (PII) before AI processing, and restrict
            access at every layer.
          </p>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold mb-6">
              🔒 Our Security Architecture
            </h2>

            <div className="space-y-8">
              <div className="border border-gray-200 dark:border-gray-800 rounded-2xl p-8">
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">
                    1
                  </div>
                  <h3 className="text-xl font-semibold">
                    Secure Upload & Storage
                  </h3>
                </div>

                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  When you upload your resume, it is securely transmitted over
                  HTTPS to our FastAPI backend. We immediately store the file in
                  encrypted Amazon S3 storage.
                </p>

                <ul className="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300">
                  <li>Encrypted data in transit (HTTPS)</li>
                  <li>Encrypted storage in Amazon S3</li>
                  <li>Restricted backend access controls</li>
                  <li>No public file exposure</li>
                </ul>

                <p className="mt-4 text-gray-700 dark:text-gray-300">
                  Resume files are not publicly accessible and are never exposed
                  to external services in raw form.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-800 rounded-2xl p-8">
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">
                    2
                  </div>
                  <h3 className="text-xl font-semibold">
                    PII Redaction Before AI Processing
                  </h3>
                </div>

                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  Before your resume content is sent to any language model, it
                  is processed by our internal redaction layer.
                </p>

                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  We use server-side PII detection logic to automatically remove
                  or mask sensitive information such as:
                </p>

                <ul className="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300">
                  <li>Full names</li>
                  <li>Email addresses</li>
                  <li>Phone numbers</li>
                  <li>Physical addresses</li>
                  <li>Identification numbers</li>
                </ul>

                <p className="mt-4 text-gray-700 dark:text-gray-300">
                  This redaction process runs inside our backend before any AI
                  call is made. The AI model never receives your raw personal
                  identifiers.
                </p>
              </div>

              <div className="border border-gray-200 dark:border-gray-800 rounded-2xl p-8">
                <div className="flex items-center gap-4 mb-4">
                  <div className="text-3xl font-bold text-indigo-600 dark:text-indigo-400">
                    3
                  </div>
                  <h3 className="text-xl font-semibold">
                    AI Processes Only Anonymized Content
                  </h3>
                </div>

                <p className="text-gray-700 dark:text-gray-300 mb-4">
                  The AI model receives only the redacted version of your
                  resume.
                </p>

                <ul className="list-disc pl-6 space-y-2 text-gray-700 dark:text-gray-300">
                  <li>Job responsibilities and achievements</li>
                  <li>Skills and technical competencies</li>
                  <li>Education details (without identifiers)</li>
                  <li>Project descriptions</li>
                  <li>Resume structure and formatting</li>
                </ul>

                <p className="mt-4 text-gray-700 dark:text-gray-300">
                  This allows us to generate high-quality feedback while
                  minimizing exposure of sensitive data.
                </p>
              </div>
            </div>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold mb-6">
              🛡 Infrastructure & Access Controls
            </h2>

            <ul className="space-y-4 text-gray-700 dark:text-gray-300">
              <li>• Server-side processing using FastAPI</li>
              <li>• Rate limiting using Redis to prevent abuse</li>
              <li>• Structured metadata storage in PostgreSQL</li>
              <li>• No selling or sharing of user data</li>
              <li>• Limited administrative access</li>
            </ul>
          </section>

          <section className="mb-16">
            <h2 className="text-2xl font-semibold mb-8">Why This Matters</h2>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="border border-green-200 dark:border-green-800 rounded-2xl p-6">
                <h3 className="text-green-600 dark:text-green-400 font-semibold mb-4">
                  ✅ What ResumeRoast Does
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Redacts PII before AI processing</li>
                  <li>• Encrypts files in storage</li>
                  <li>• Restricts backend access</li>
                  <li>• Minimizes raw data exposure</li>
                </ul>
              </div>

              <div className="border border-red-200 dark:border-red-800 rounded-2xl p-6">
                <h3 className="text-red-600 dark:text-red-400 font-semibold mb-4">
                  ❌ What Many Tools Do
                </h3>
                <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                  <li>• Send raw resumes directly to AI APIs</li>
                  <li>• Store unredacted personal data</li>
                  <li>• Lack clear access controls</li>
                  <li>• Provide no transparency about data flow</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-6">Our Commitment</h2>

            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
              ResumeRoast is built with a privacy-first mindset. While no
              internet system can claim absolute security, we intentionally
              designed our architecture to minimize data exposure, redact
              personal information before AI processing, and restrict access to
              sensitive content.
            </p>
          </section>
        </div>
      </main>
    </>
  );
}
