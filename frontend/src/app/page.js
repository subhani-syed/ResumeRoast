"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import Navbar from "@/components/Navbar";
import Link from "next/link";

const faqs = [
  {
    question: "Is my resume safe?",
    answer:
      "Yes. Your resume is transmitted securely, stored in encrypted cloud storage, and processed through our server-side redaction layer before any AI analysis occurs. The AI model never receives your raw personal identifiers.",
  },
  {
    question: "Does the AI see my name, email, or phone number?",
    answer:
      "No. Before sending your resume content to the language model, we automatically redact personally identifiable information (PII) such as names, emails, phone numbers, and addresses. The AI only analyzes anonymized content.",
  },
  {
    question: "Do we store your resume?",
    answer:
      "Your resume file is securely stored in encrypted cloud storage to enable processing and results delivery. We do not sell your data or share it with third parties. Access to stored data is restricted and controlled.",
  },
  {
    question: "How is ResumeRoast different from other AI resume tools?",
    answer:
      "Many tools send raw resumes directly to AI APIs. ResumeRoast adds a privacy layer, we redact sensitive information before AI processing and minimize raw data exposure within our backend.",
  },
  {
    question: "Is ResumeRoast free?",
    answer:
      "ResumeRoast offers limited free usage with rate limits to prevent abuse. This allows you to try the product while ensuring fair usage across users.",
  },
];

export default function LandingPage() {
  const [openIndex, setOpenIndex] = useState(null);
  const navItems = [
    { label: "Features", href: "/#features" },
    { label: "Reviews", href: "/#reviews" },
    { label: "FAQ", href: "/#faq" },
    { label: "How It Works", href: "/privacy" },
  ];

  return (
    <>
      <Navbar
        items={navItems}
        rightComponent={
          <Link
            href="/home"
            className="px-6 py-2 rounded bg-linear-to-r from-blue-500 to-cyan-500 text-sm font-semibold hover:opacity-90 transition"
          >
            Get Started
          </Link>
        }
      />
      <main className="bg-black/60 min-h-screen">
        <div className="absolute inset-0 -z-10  blur-3xl" />
        <section className="text-center px-6 pt-24 pb-32 max-w-4xl mx-auto">
          <h2 className="text-5xl md:text-7xl font-extrabold leading-tight ">
            Your Resume Isn’t That Good.
            <br />
            <span className="bg-linear-to-r from-blue-400 to-cyan-500 bg-clip-text text-transparent">
              Let AI Roast It.
            </span>
          </h2>

          <p className="mt-8 text-lg max-w-2xl mx-auto ">
            Brutally honest AI-powered resume reviews that expose weaknesses,
            fluff, and missed opportunities, so recruiters don’t.
          </p>

          <div className="mt-10 flex justify-center gap-4">
            <Link
              href="/home"
              className="px-8 py-4 rounded-2xl bg-linear-to-r from-blue-400 to-cyan-500 text-lg text-white font-semibold hover:scale-105 transition"
            >
              Roast My Resume 🔥
            </Link>
            <button className="px-8 py-4 rounded-2xl border border-gray-700 hover:bg-white hover:text-black transition">
              See Example
            </button>
          </div>
        </section>

        <section className="px-6 py-24 bg-white/5 backdrop-blur-sm border-y border-white/10">
          <div className="max-w-6xl mx-auto grid md:grid-cols-2 gap-16 items-center">
            <div>
              <h3 className="text-4xl font-bold mb-6">
                Powered by Advanced AI
              </h3>
              <p className="text-gray-300 text-lg leading-relaxed">
                ResumeRoast uses cutting-edge AI models trained on hiring
                patterns, recruiter psychology, and ATS behavior to give you
                actionable feedback, not generic advice.
              </p>
            </div>

            <div className="bg-linear-to-br from-blue-500/20 to-cyan-500/20 p-8 rounded border border-white/10">
              <h4 className="text-2xl font-semibold mb-4">🔐 Privacy First</h4>
              <p className="text-white">
                Before your resume is analyzed, we automatically redact all
                personally identifiable information, including name, phone,
                email, and address.
              </p>
              <p className="text-gray-300 mt-4">
                Your identity stays safe. Only your content gets roasted.
              </p>
            </div>
          </div>
        </section>

        <section className="px-6 py-28" id="reviews">
          <div className="max-w-6xl mx-auto text-center">
            <h3 className="text-4xl font-bold mb-16">Loved by Job Seekers</h3>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  name: "Pam H.",
                  review:
                    "I thought my resume was strong. ResumeRoast humbled me. Got 3 interviews after fixing it.",
                },
                {
                  name: "Kelly K.",
                  review:
                    "Brutal but accurate. The AI spotted fluff I didn’t even realize was there.",
                },
                {
                  name: "Angela S.",
                  review: "The roast was hilarious and genuinely helpful.",
                },
              ].map((item, index) => (
                <div
                  key={index}
                  className="bg-white/5 border border-white/10 p-8 rounded hover:bg-white/10 transition"
                >
                  <p className="text-gray-300 mb-6">“{item.review}”</p>
                  <h4 className="font-semibold text-cyan-400">{item.name}</h4>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="px-6 p-10 max-w-4xl mx-auto" id="faq">
          <h3 className="text-4xl font-bold text-center mb-12">
            Frequently Asked Questions
          </h3>

          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div
                key={index}
                className="border border-white/10 rounded bg-white/5"
              >
                <button
                  className="w-full flex justify-between items-center p-6 text-left"
                  onClick={() =>
                    setOpenIndex(openIndex === index ? null : index)
                  }
                >
                  <span className="font-medium">{faq.question}</span>
                  <ChevronDown
                    className={`transition-transform ${
                      openIndex === index ? "rotate-180" : ""
                    }`}
                  />
                </button>

                {openIndex === index && (
                  <div className="px-6 pb-6 text-gray-400">{faq.answer}</div>
                )}
              </div>
            ))}
          </div>
        </section>

        <section className="text-center pb-24">
          <h3 className="text-5xl font-bold mb-8">Ready to Face the Truth?</h3>
          <Link
            href="/home"
            className="px-10 py-5 rounded bg-linear-to-r from-blue-500 to-cyan-500 text-xl font-semibold hover:scale-105 transition"
          >
            Roast My Resume Now 🔥
          </Link>
        </section>

        <footer className="border-t border-white/10 py-10 px-6 text-center text-gray-300">
          <p>© {new Date().getFullYear()} ResumeRoast. All rights reserved.</p>
          <p className="mt-2 text-sm">Built with AI. Designed for honesty.</p>
        </footer>
      </main>
    </>
  );
}
