import { ArrowRight, Sparkles, Globe2, Mic, Shield, Languages, Mail, Heart, BookOpen, Users } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const highlights = [
  {
    title: "Voice Activated",
    description: "Natural conversation in Nordic languages with wake word activation",
    icon: <Mic className="h-6 w-6" />,
    color: "from-purple-500 to-purple-600"
  },
  {
    title: "5 Nordic Languages",
    description: "English, Swedish, Danish, Norwegian, Finnish - perfectly localized",
    icon: <Languages className="h-6 w-6" />,
    color: "from-blue-500 to-cyan-500"
  },
  {
    title: "Privacy & Safety First",
    description: "GDPR compliant, kid-safe, built specifically for Nordic families",
    icon: <Shield className="h-6 w-6" />,
    color: "from-green-500 to-emerald-600"
  },
  {
    title: "Story Creation",
    description: "AI-powered storytelling that creates personalized tales for your child",
    icon: <BookOpen className="h-6 w-6" />,
    color: "from-orange-500 to-red-500"
  },
  {
    title: "Educational Content",
    description: "Age-appropriate learning through playful interaction (4-12 years)",
    icon: <Sparkles className="h-6 w-6" />,
    color: "from-pink-500 to-rose-600"
  },
  {
    title: "Nordic Design",
    description: "Born in Gothenburg, Sweden - designed with Nordic values",
    icon: <Heart className="h-6 w-6" />,
    color: "from-indigo-500 to-purple-600"
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
        <div className="absolute left-1/2 top-1/2 h-96 w-96 animate-pulse rounded-full bg-pink-200/20 blur-3xl delay-500" />
      </div>

      {/* Header */}
      <header className="mx-auto flex w-full max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <div className="flex items-center gap-3">
          <Image
            src="/logo.svg"
            alt="Sagatoy"
            width={200}
            height={67}
            className="h-16 w-auto"
            priority
          />
        </div>
      </header>

      {/* Main Content */}
      <section className="mx-auto flex min-h-[80vh] max-w-7xl items-center px-6 lg:px-8 py-12">
        <div className="grid w-full gap-12 lg:grid-cols-2 lg:items-center">
          {/* Left Column - Hero Content */}
          <div className="space-y-8">
            <div className="inline-flex items-center gap-2 rounded-full border border-saga-purple/20 bg-saga-purple/10 px-4 py-2 text-sm font-semibold text-saga-purple shadow-sm">
              <Globe2 className="h-4 w-4" />
              Coming Soon to Nordic Families
            </div>

            <h2 className="font-display text-5xl font-bold leading-tight text-saga-ink lg:text-6xl">
              Your Child&apos;s <br />
              <span className="bg-gradient-to-r from-saga-purple to-saga-sky bg-clip-text text-transparent">
                AI Companion
              </span>
            </h2>

            <p className="text-xl leading-relaxed text-slate-600">
              We&apos;re building something truly special for Nordic families with kids aged 4-12.
              Sagatoy is an intelligent toy companion that speaks 5 Nordic languages and helps children learn through natural, engaging conversation.
            </p>

            <p className="text-lg leading-relaxed text-slate-600">
              Transform any classic plush toy into an AI-powered friend. No screens, no apps—just pure conversational magic powered by cutting-edge AI technology, designed with Nordic values of safety, privacy, and meaningful play.
            </p>

            {/* Features List */}
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-saga-ink uppercase tracking-wide">What Makes Sagatoy Special:</h3>
              <ul className="space-y-2 text-slate-600">
                <li className="flex items-start gap-2">
                  <span className="text-saga-purple">✓</span>
                  <span><strong>Natural Conversation:</strong> Talks like a real friend, not a robot</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-saga-purple">✓</span>
                  <span><strong>5 Nordic Languages:</strong> English, Swedish, Danish, Norwegian, Finnish</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-saga-purple">✓</span>
                  <span><strong>Wake Word Activation:</strong> No apps or screens needed—just say &quot;Hey Sagatoy!&quot;</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-saga-purple">✓</span>
                  <span><strong>Privacy First:</strong> GDPR compliant, data encrypted, parent-controlled</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-saga-purple">✓</span>
                  <span><strong>Story Creation:</strong> Generates personalized bedtime stories on demand</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-saga-purple">✓</span>
                  <span><strong>Educational:</strong> Teaches while playing—perfect for ages 4-12</span>
                </li>
              </ul>
            </div>

            {/* Status Badge */}
            <div className="glass inline-flex items-center gap-3 rounded-2xl border border-white/60 bg-white/90 px-6 py-4 shadow-lg backdrop-blur">
              <div className="flex h-3 w-3 items-center justify-center">
                <span className="absolute inline-flex h-3 w-3 animate-ping rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex h-2 w-2 rounded-full bg-green-500"></span>
              </div>
              <div>
                <p className="text-sm font-semibold text-saga-ink">Currently in Development</p>
                <p className="text-xs text-slate-500">Launching Q2 2025</p>
              </div>
            </div>

            {/* Email Signup */}
            <div className="space-y-3">
              <p className="text-sm font-medium text-slate-700">Get notified when we launch:</p>
              <form className="flex max-w-md gap-3">
                <input
                  type="email"
                  placeholder="your@email.com"
                  className="flex-1 rounded-full border-2 border-slate-200 bg-white px-5 py-3 text-sm transition focus:border-saga-purple focus:outline-none"
                />
                <button
                  type="submit"
                  className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-saga-purple to-saga-sky px-6 py-3 font-semibold text-white shadow-lg transition hover:scale-105 hover:shadow-xl"
                >
                  <Mail className="h-4 w-4" />
                  Notify Me
                </button>
              </form>
              <p className="text-xs text-slate-500">
                We respect your privacy. Unsubscribe at any time.
              </p>
            </div>
          </div>

          {/* Right Column - Image */}
          <div className="relative">
            <div className="glass relative overflow-hidden rounded-3xl p-8 shadow-2xl">
              <div className="absolute -right-12 -top-12 h-48 w-48 rounded-full bg-gradient-to-br from-saga-purple/20 to-transparent blur-2xl" />
              <div className="absolute -bottom-12 -left-12 h-48 w-48 rounded-full bg-gradient-to-tr from-saga-sky/20 to-transparent blur-2xl" />

              <div className="relative aspect-square overflow-hidden rounded-2xl bg-gradient-to-br from-slate-100 to-slate-50">
                <Image
                  src="/sagatoy.jpeg"
                  alt="Sagatoy AI companion"
                  fill
                  className="object-cover"
                  priority
                />
              </div>

              {/* Floating badges */}
              <div className="absolute right-4 top-4 rounded-2xl border border-white/60 bg-white/90 px-4 py-3 shadow-lg backdrop-blur">
                <div className="flex items-center gap-2">
                  <Globe2 className="h-5 w-5 text-saga-sky" />
                  <span className="text-sm font-semibold text-saga-ink">5 Languages</span>
                </div>
              </div>

              <div className="absolute left-4 bottom-4 rounded-2xl border border-white/60 bg-white/90 px-4 py-3 shadow-lg backdrop-blur">
                <div className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-saga-purple" />
                  <span className="text-sm font-semibold text-saga-ink">AI Powered</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Preview */}
      <section className="mx-auto max-w-7xl px-6 py-16 lg:px-8">
        <div className="text-center mb-12">
          <h3 className="font-display text-3xl font-bold text-saga-ink mb-3">
            What to Expect
          </h3>
          <p className="text-lg text-slate-600">
            Comprehensive features designed for Nordic families
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {highlights.map((item) => (
            <div key={item.title} className="glass rounded-2xl p-8 text-center transition hover:shadow-xl group">
              <div className={`mx-auto mb-4 inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br ${item.color} text-white shadow-lg transition group-hover:scale-110`}>
                {item.icon}
              </div>
              <h4 className="mb-2 font-display text-xl font-bold text-saga-ink">{item.title}</h4>
              <p className="text-slate-600">{item.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Why Nordic Section */}
      <section className="mx-auto max-w-7xl px-6 py-16 lg:px-8 bg-gradient-to-b from-transparent to-slate-100/50 rounded-3xl">
        <div className="max-w-3xl mx-auto text-center space-y-6">
          <h3 className="font-display text-3xl font-bold text-saga-ink mb-4">
            Why Nordic?
          </h3>
          <p className="text-lg text-slate-600 leading-relaxed">
            Born in Gothenburg, Sweden, Sagatoy combines Nordic design principles with educational values.
            We believe technology should enhance, not replace, real human connection. That&apos;s why we&apos;ve created
            an AI companion that encourages conversation, creativity, and learning—without screens.
          </p>
          <p className="text-lg text-slate-600 leading-relaxed">
            Built for EU families with Nordic values: privacy-first, educational, safe, and designed to respect
            childhood while embracing the possibilities of AI technology.
          </p>
          <div className="flex items-center justify-center gap-8 pt-8 flex-wrap">
            <div className="text-center">
              <p className="text-4xl font-bold text-saga-purple">4-12</p>
              <p className="text-sm text-slate-600">Age Range</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-saga-sky">5</p>
              <p className="text-sm text-slate-600">Languages</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-saga-purple">100%</p>
              <p className="text-sm text-slate-600">Privacy</p>
            </div>
            <div className="text-center">
              <p className="text-4xl font-bold text-saga-sky">0</p>
              <p className="text-sm text-slate-600">Screens</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white mt-16">
        <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
          <div className="flex flex-col items-center justify-between gap-6 sm:flex-row">
            <Image
              src="/logo.svg"
              alt="Sagatoy"
              width={180}
              height={60}
              className="h-12 w-auto"
            />

            <div className="flex items-center gap-6 text-sm text-slate-600">
              <Link href="mailto:hello@sagatoy.com" className="hover:text-saga-purple transition">
                Contact
              </Link>
              <Link href="#" className="hover:text-saga-purple transition">
                About
              </Link>
              <Link href="#" className="hover:text-saga-purple transition">
                Privacy
              </Link>
            </div>
          </div>

          {/* Nordic Countries Section */}
          <div className="mt-8 border-t border-slate-200 pt-8">
            <div className="text-center mb-4">
              <h4 className="text-sm font-semibold text-saga-ink mb-2">Supporting Nordic Families</h4>
              <p className="text-xs text-slate-500">Available in 5 Nordic Countries</p>
            </div>
            <div className="flex items-center justify-center gap-6 flex-wrap">
              <div className="text-center">
                <div className="text-4xl mb-1">🇸🇪</div>
                <p className="text-xs text-slate-600 font-medium">Sweden</p>
                <p className="text-xs text-slate-400">Svenska</p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-1">🇩🇰</div>
                <p className="text-xs text-slate-600 font-medium">Denmark</p>
                <p className="text-xs text-slate-400">Dansk</p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-1">🇳🇴</div>
                <p className="text-xs text-slate-600 font-medium">Norway</p>
                <p className="text-xs text-slate-400">Norsk</p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-1">🇫🇮</div>
                <p className="text-xs text-slate-600 font-medium">Finland</p>
                <p className="text-xs text-slate-400">Suomi</p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-1">🇬🇧</div>
                <p className="text-xs text-slate-600 font-medium">English</p>
                <p className="text-xs text-slate-400">International</p>
              </div>
            </div>
          </div>

          <div className="mt-8 border-t border-slate-200 pt-6 text-center text-sm text-slate-500">
            <p>© {new Date().getFullYear()} Sagatoy. All rights reserved.</p>
            <p className="mt-2 text-xs flex items-center justify-center gap-1">
              Made with <Heart className="h-3 w-3 text-red-500 fill-red-500" /> in Gothenburg, Sweden 🇸🇪
            </p>
          </div>
        </div>
      </footer>
    </main>
  );
}
