<script>

import AddMember from "$lib/group/member/AddMember.svelte";
import MemberList from "$lib/group/member/MemberList.svelte";
export let groupname;
export let groupmembers;
</script>

<div>
<AddMember groupname={groupname}/>
<MemberList groupname={groupname} groupmembers={groupmembers} />
</div>

<style>
    div {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        justify-content: flex-start;
        height: max-content;
        gap: 2em;
    }
</style>
