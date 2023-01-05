$(function() {
	var documentHash = document.location.hash.substring(1, document.location.hash.length);

	if(documentHash !== '')
	{
		var changelogResults = $('*[data-version="' + encodeURI(documentHash) + '"]');

		if(changelogResults.length === 0)
		{
			$.notify('No changelog found for version "' + documentHash + '".', {
				className: 'error',
				globalPosition: 'top right',
				autoHide: false
			});
		}
	}
});
