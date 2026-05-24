function Link(el)
	if FORMAT:match("latex") then
		-- If the visible text equals the URL, render as \url{} which breaks properly
		local text = pandoc.utils.stringify(el.content)
		if text == el.target then
			return pandoc.RawInline("latex", "\\url{" .. el.target .. "}")
		end
	end
end
