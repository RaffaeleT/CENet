import { Link } from "react-router";

export default function SidebarWidget() {
  return (
    <div className="mt-auto p-4 border-t border-gray-200 dark:border-gray-700">
      <div className="flex items-center gap-3">
        <img
          src="/images/user/owner.jpg"
          alt="User"
          className="h-10 w-10 rounded-full object-cover"
        />
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
            Musharof Chowdhury
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
            randomuser@pimjo.com
          </p>
        </div>
      </div>
      <div className="mt-3">
        <Link
          to="/profile"
          className="flex text-center px-3 py-2 text-xs font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 dark:text-gray-300 dark:bg-gray-800 dark:hover:bg-gray-700 transition-colors justify-center"
        >
          Profile
        </Link>
      </div>
    </div>
  );
}