def version_in_range(version, min_version, max_version):
    # Ensure version numbers are strings
    version = str(version)
    min_version = str(min_version)
    max_version = str(max_version)
    
    # Check if the supplied versions have dots
    if '.' not in version:
        versionArr = [int(version)]
    else:
        versionArr = [int(v) for v in version.split('.')]
        
    if '.' not in min_version:
        min_versionArr = [int(min_version)]
    else:
        min_versionArr = [int(v) for v in min_version.split('.')]
        
    if '.' not in max_version:
        max_versionArr = [int(max_version)]
    else:
        max_versionArr = [int(v) for v in max_version.split('.')]

    for i in range(len(versionArr)):
        v = versionArr[i]
        min_v = min_versionArr[i] if i < len(min_versionArr) else 0
        max_v = max_versionArr[i] if i < len(max_versionArr) else float('inf')
    
        
        if not (min_v <= v <= max_v):

            return False
    
    return True