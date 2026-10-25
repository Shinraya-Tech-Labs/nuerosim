import "./style.css";
export const metadata = {
  title: "NeuroSim | Scientific workspace",
  description: "Recorded neural networks and reproducible CPU experiments",
};
export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
