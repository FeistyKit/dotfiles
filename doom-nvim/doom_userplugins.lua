-- doom_userplugins - Doom nvim custom plugins
--
-- This file contains all the custom plugins that are not in Doom nvim but that
-- the user requires. All the available fields can be found here
-- https://github.com/wbthomason/packer.nvim#specifying-plugins
--
-- By example, for including a plugin with a dependency on telescope:
-- M.plugins {
--   {
--     'user/repository',
--     requires = { 'nvim-lua/telescope.nvim' },
--   },
-- }

local M = {}

M.source = debug.getinfo(1, "S").source:sub(2)

M.plugins = {
	"chriskempson/base16-vim",
	"alaviss/nim.nvim",
	"tikhomirov/vim-glsl",
	"catppuccin/nvim",
})"RRethy/nvim-align"
}

-- Set up language server for nim
require 'lspconfig'.nimls.setup{}
-- Set up language server for haskell
require'lspconfig'.hls.setup{}

return M

-- vim: sw=2 sts=2 ts=2 noexpandtab
