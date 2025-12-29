import { ArrowRight, Sparkles, Globe2, Mic, Shield, Languages, Mail } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const highlights = [
  {
    title: "Voice Activated",
    description: "Natural conversation in Nordic languages",
    icon: <Mic className="h-6 w-6" />
  },
  {
    title: "5 Languages",
    description: "English, Swedish, Danish, Norwegian, Finnish",
    icon: <Languages className="h-6 w-6" />
  },
  {
    title: "Privacy First",
    description: "GDPR compliant, built for Nordic families",
    icon: <Shield className="h-6 w-6" />
  }
];

export default function Page() {
  return (
    <main className="relative isolate min-h-screen overflow-hidden bg-gradient-to-b from-slate-50 via-white to-slate-50">
      {/* Animated background */}
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(139,92,246,0.15),transparent_40%),radial-gradient(circle_at_80%_80%,rgba(56,189,248,0.15),transparent_40%)]" />
        <div className="absolute left-1/4 top-1/4 h-96 w-96 animate-pulse rounded-full bg-purple-200/20 blur-3xl" />
        <div className="absolute right-1/4 bottom-1/4 h-96 w-96 animate-pulse rounded-full bg-sky-200/20 blur-3xl delay-1000" />
      </div>

      {/* Header */}
      <header className="mx-auto w-full max-w-7xl px-6 py-8 lg:px-8">
        <nav className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Image
              src="/logo.png"
              alt="Sagatoy"
              width={60}
              height={60}
              className="h-14 w-auto"
              priority
            />
            <div>
              <h1 className="text-2xl font-bold text-saga-ink">Sagatoy</h1>
              <p className="text-xs text-slate-500">AI Companion for Kids</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-6 text-sm text-slate-600">
            <Link href="#features" className="hover:text-saga-purple transition">Features</Link>
            <Link href="#about" className="hover:text-saga-purple transition">About</Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="mx-auto max-w-7xl px-6 pt-16 pb-24 lg:px-8 lg:pt-24">
        <div className="grid gap-16 lg:grid-cols-12 lg:gap-8">
          {/* Left Column - Hero Content */}
          <div className="lg:col-span-7 flex flex-col justify-center space-y-8">
            <div className="space-y-6">
              <div className="inline-flex items-center gap-2 rounded-full border border-saga-purple/20 bg-saga-purple/5 px-4 py-1.5 text-sm font-medium text-saga-purple">
                <Globe2 className="h-3.5 w-3.5" />
                Coming Soon to Nordic Families
              </div>

              <h1 className="font-display text-5xl font-bold leading-[1.1] tracking-tight text-saga-ink lg:text-7xl">
                AI Companion{" "}
                <span className="bg-gradient-to-r from-saga-purple via-blue-600 to-saga-sky bg-clip-text text-transparent">
                  For Your Child
                </span>
              </h1>

              <p className="text-lg leading-relaxed text-slate-600 max-w-2xl">
                An intelligent toy companion that speaks Nordic languages and helps children aged 4-12 learn through natural conversation.
              </p>
            </div>

            {/* Email Signup */}
            <div className="space-y-4">
              <form className="flex flex-col sm:flex-row gap-3 max-w-lg">
                <input
                  type="email"
                  placeholder="your@email.com"
                  className="flex-1 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm transition focus:border-saga-purple focus:outline-none focus:ring-2 focus:ring-saga-purple/20"
                />
                <button
                  type="submit"
                  className="inline-flex items-center justify-center gap-2 rounded-xl bg-saga-ink px-6 py-3 font-semibold text-white shadow-lg transition hover:bg-saga-ink/90 hover:shadow-xl"
                >
                  <Mail className="h-4 w-4" />
                  Get Early Access
                </button>
              </form>
              <p className="text-xs text-slate-500">
                Join the waitlist • Launching Q2 2025
              </p>
            </div>

            {/* Status Badge */}
            <div className="inline-flex items-center gap-3 rounded-xl border border-slate-200 bg-white/80 px-4 py-3 shadow-sm backdrop-blur w-fit">
              <div className="flex h-2 w-2 items-center justify-center">
                <span className="absolute inline-flex h-2 w-2 animate-ping rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-green-500"></span>
              </div>
              <p className="text-sm font-medium text-saga-ink">Currently in Development</p>
            </div>
          </div>

          {/* Right Column - Image */}
          <div className="lg:col-span-5 flex items-center">
            <div className="relative w-full">
              <div className="absolute -inset-4 rounded-3xl bg-gradient-to-r from-saga-purple/20 to-saga-sky/20 blur-2xl opacity-50" />
              <div className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-2 shadow-2xl">
                <div className="relative aspect-square overflow-hidden rounded-xl bg-gradient-to-br from-slate-50 to-slate-100">
                  <Image
                    src="/sagatoy.jpeg"
                    alt="Sagatoy AI companion"
                    fill
                    className="object-cover"
                    priority
                  />
                </div>
                {/* Floating badge */}
                <div className="absolute right-6 top-6 rounded-lg border border-white/60 bg-white/95 px-3 py-2 shadow-lg backdrop-blur-sm">
                  <div className="flex items-center gap-2">
                    <Globe2 className="h-4 w-4 text-saga-sky" />
                    <span className="text-sm font-semibold text-saga-ink">5 Languages</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Preview */}
      <section id="features" className="mx-auto max-w-7xl px-6 py-24 lg:px-8 bg-gradient-to-b from-transparent to-slate-50/50">
        <div className="text-center mb-16 space-y-4">
          <h2 className="font-display text-4xl font-bold text-saga-ink lg:text-5xl">
            Built for Nordic Families
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            A magical learning companion designed specifically for children in the Nordics
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-3">
          {highlights.map((item) => (
            <div key={item.title} className="group relative rounded-2xl border border-slate-200 bg-white p-8 shadow-sm transition hover:shadow-lg hover:border-saga-purple/30">
              <div className="mb-6 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-saga-purple to-saga-sky text-white shadow-md">
                {item.icon}
              </div>
              <h3 className="mb-3 text-xl font-bold text-saga-ink">{item.title}</h3>
              <p className="text-slate-600 leading-relaxed">{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white/50 backdrop-blur-sm">
        <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
          <div className="grid gap-8 md:grid-cols-3">
            {/* Logo & Tagline */}
            <div className="space-y-4">
              <div className="flex items-center gap-2">
                <Image
                  src="/logo.png"
                  alt="Sagatoy"
                  width={50}
                  height={50}
                  className="h-12 w-auto"
                />
                <div>
                  <h2 className="text-lg font-bold text-saga-ink">Sagatoy</h2>
                  <p className="text-xs text-slate-500">AI Companion for Kids</p>
                </div>
              </div>
              <p className="text-sm text-slate-600 leading-relaxed">
                Making learning magical for Nordic children aged 4-12.
              </p>
            </div>

            {/* Quick Links */}
            <div>
              <h3 className="text-sm font-semibold text-saga-ink mb-4">Product</h3>
              <ul className="space-y-3 text-sm text-slate-600">
                <li><Link href="#features" className="hover:text-saga-purple transition">Features</Link></li>
                <li><Link href="#about" className="hover:text-saga-purple transition">About</Link></li>
                <li><span className="text-slate-400">Pricing (Coming Soon)</span></li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h3 className="text-sm font-semibold text-saga-ink mb-4">Contact</h3>
              <ul className="space-y-3 text-sm text-slate-600">
                <li>
                  <Link href="mailto:hello@sagatoy.com" className="hover:text-saga-purple transition">
                    hello@sagatoy.com
                  </Link>
                </li>
                <li className="text-slate-500">Gothenburg, Sweden 🇸🇪</li>
              </ul>
            </div>
          </div>

          <div className="mt-8 border-t border-slate-200 pt-8 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-slate-500">
            <p>© {new Date().getFullYear()} Sagatoy. All rights reserved.</p>
            <p className="text-xs">Made with care in Sweden</p>
          </div>
        </div>
      </footer>
    </main>
  );
}
