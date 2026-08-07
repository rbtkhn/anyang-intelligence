import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Grace Mar | Coming Soon",
  description:
    "Grace Mar is a considered commercial house and home to Grace Gems, its flagship jewelry brand.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
