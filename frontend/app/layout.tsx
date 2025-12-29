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
  title: "Sagatoy | Nordic AI Companion for Kids",
  description: "Transform classic plush toys into AI-powered friends that speak 5 Nordic languages. Perfect for kids aged 4-12. Wake word activated, no apps needed."
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
