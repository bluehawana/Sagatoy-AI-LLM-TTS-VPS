import "./globals.css";
import type { Metadata } from "next";
import { Inter, Space_Grotesk } from "next/font/google";
import { clsx } from "clsx";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const spaceGrotesk = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space-grotesk"
});

export const metadata: Metadata = {
  title: "SagaToy | AI Storytelling Companion",
  description: "SagaToy is the magical AI storytelling friend for kids. Under construction — coming soon."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={clsx(inter.variable, spaceGrotesk.variable, "antialiased min-h-screen")}>
        {children}
      </body>
    </html>
  );
}
