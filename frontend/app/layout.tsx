import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CivicFix | Community issue reporting",
  description: "Report and track local infrastructure issues with clear, structured information.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

