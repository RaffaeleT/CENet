export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white mt-16">
      <div className="max-w-7xl mx-auto px-6 py-10">
        
        {/* Top section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          
          {/* Logo + description */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <img
                src="/images/logo/logo-icon.png"
                alt="CENet"
                className="h-8 w-8"
              />
              <span className="font-semibold text-gray-800">
                CENet Energy HUB
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Empowering energy communities through smart tools, simulations, and collaboration.
            </p>
          </div>

          {/* Contact */}
          <div>
            <h4 className="text-sm font-semibold text-gray-800 mb-3">
              Contact
            </h4>
            <p className="text-sm text-gray-500">
              Email:{" "}
              <a
                href="mailto:connect@cenet.it"
                className="text-[#159570] hover:underline"
              >
                connect@cenet.it
              </a>
            </p>
          </div>

          {/* Social / LinkedIn */}
          <div>
            <h4 className="text-sm font-semibold text-gray-800 mb-3">
              Follow us
            </h4>
            <a
              href="https://www.linkedin.com"
              target="_blank"
              className="flex items-center gap-2 text-sm text-gray-500 hover:text-[#159570]"
            >
              <img
                src="/images/brand/brand-16.svg"
                alt="LinkedIn"
                className="h-4 w-4"
              />
              LinkedIn
            </a>
          </div>
        </div>

        {/* Bottom section */}
        <div className="mt-10 pt-6 border-t border-gray-100 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-xs text-gray-400">
            © {new Date().getFullYear()} CENet Energy HUB. All rights reserved.
          </p>

          <div className="flex gap-4 text-xs text-gray-400">
            <a href="#" className="hover:text-[#159570]">
              Privacy Policy
            </a>
            <a href="#" className="hover:text-[#159570]">
              Terms
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}